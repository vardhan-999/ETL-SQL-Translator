import sys
import os


import streamlit as st
import pandas as pd
import json
from src.sql_reader import parse_streamlit_upload
from src.dialect_detector import detect_dialect
from src.sql_translator import translate_sql
from src.llm_agent import get_llm_translation_and_issues
from src.validator import validate_sql
from src.report_generator import generate_markdown_report, generate_issues_json
from src.database import log_migration, get_history, clear_history

# Page Configuration
st.set_page_config(page_title="ETL SQL Translator", page_icon="🔄", layout="wide")

# Custom CSS for a professional look
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    /* Glassmorphism sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        border: none;
        color: white;
    }
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 8px;
    }
    .status-badge-success {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        padding: 6px 12px;
        border-radius: 9999px;
        font-weight: bold;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .status-badge-fail {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        padding: 6px 12px;
        border-radius: 9999px;
        font-weight: bold;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🔄 ETL SQL Translator")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["SQL Translator", "Migration History"])

if page == "SQL Translator":
    st.title("SQL Translation Engine")
    st.markdown("Upload SQL files to automatically convert them between dialects using AI-assisted translation.")
    
    col1, col2 = st.columns(2)
    with col1:
        source_dialect = st.selectbox("Source Dialect", ["Auto-detect", "mysql", "postgres", "sqlite"])
    with col2:
        target_dialect = st.selectbox("Target Dialect", ["postgres", "mysql", "sqlite"])
        
    upload_method = st.radio("File Input Method", ["Upload via Browser", "Local File Path (Best for Large Files)"])
    
    uploaded_files = []
    local_files = []
    
    if upload_method == "Upload via Browser":
        uploaded_files = st.file_uploader("Upload SQL Files", type=["sql", "txt"], accept_multiple_files=True)
    else:
        file_path = st.text_input("Enter absolute path to the local SQL file:")
        if file_path:
            if os.path.exists(file_path):
                class LocalFile:
                    def __init__(self, path):
                        self.name = os.path.basename(path)
                        self.path = path
                    def getvalue(self):
                        with open(self.path, 'rb') as f:
                            return f.read()
                local_files = [LocalFile(file_path)]
            else:
                st.error("File not found.")
                
    files_to_process = uploaded_files if upload_method == "Upload via Browser" else local_files
    
    if st.button("🚀 Start SQL Migration"):
        if not files_to_process:
            st.warning("Please provide at least one SQL file.")
        else:
            for uploaded_file in files_to_process:
                st.markdown("---")
                st.subheader(f"File: {uploaded_file.name}")
                
                # 1. Read File
                sql_content = parse_streamlit_upload(uploaded_file)
                
                # 2. Detect Dialect
                actual_source = source_dialect
                if source_dialect == "Auto-detect":
                    actual_source = detect_dialect(sql_content)
                    st.info(f"Detected Source Dialect: **{actual_source}**")
                
                if actual_source == "unknown":
                    st.error("Could not detect source dialect. Please select it manually.")
                    continue
                
                # 3. Translation Engine
                with st.spinner("Translating using SQLGlot..."):
                    translated_sql, is_success, error_msg = translate_sql(sql_content, actual_source, target_dialect)
                
                ai_response = {}
                final_translated_sql = translated_sql
                status = "SUCCESS"
                issues = []
                
                # 4. LLM Fallback (if SQLGlot fails or raises warnings)
                if not is_success:
                    st.error(f"🚨 **Syntax Error Detected in Original SQL:**\n\n`{error_msg}`")
                    st.warning("Engaging AI Agent to attempt a manual fix and translation...")
                    with st.spinner("Analyzing with LLM..."):
                        ai_response = get_llm_translation_and_issues(sql_content, actual_source, target_dialect, error_msg)
                        final_translated_sql = ai_response.get("translated_sql", "")
                        issues = ai_response.get("issues_detected", [])
                        status = "PARTIAL" if final_translated_sql else "FAILED"
                else:
                    if final_translated_sql.strip() == sql_content.strip():
                        st.info("ℹ️ The target dialect uses identical syntax for this query.")
                
                # 5. Validation
                if final_translated_sql:
                    val_status, val_message = validate_sql(final_translated_sql, target_dialect)
                    if val_status == "FAILED":
                        status = "FAILED"
                        issues.append(f"Validation Error: {val_message}")
                
                # Display Results
                col_orig, col_trans = st.columns(2)
                
                # Truncate for display to prevent browser out-of-memory errors on large files
                MAX_DISPLAY_CHARS = 5000
                
                display_orig = sql_content
                if len(display_orig) > MAX_DISPLAY_CHARS:
                    display_orig = display_orig[:MAX_DISPLAY_CHARS] + f"\n\n-- ... truncated {len(display_orig) - MAX_DISPLAY_CHARS} characters for UI preview ... --"
                    
                display_trans = final_translated_sql
                if len(display_trans) > MAX_DISPLAY_CHARS:
                    display_trans = display_trans[:MAX_DISPLAY_CHARS] + f"\n\n-- ... truncated {len(display_trans) - MAX_DISPLAY_CHARS} characters for UI preview ... --"

                with col_orig:
                    st.markdown("**Original SQL (Preview)**")
                    st.code(display_orig, language="sql")
                with col_trans:
                    st.markdown("**Translated SQL (Preview)**")
                    st.code(display_trans, language="sql")
                    
                # Badges
                if status == "SUCCESS":
                    st.markdown("<span class='status-badge-success'>Validation: PASS</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='status-badge-fail'>Validation: {status}</span>", unsafe_allow_html=True)
                    
                # AI Suggestions Expander
                if ai_response:
                    with st.expander("🤖 AI Suggestions & Issues", expanded=True):
                        st.write(f"**Confidence:** {ai_response.get('confidence_score')}")
                        st.write(f"**Explanation:** {ai_response.get('explanation')}")
                        if ai_response.get('issues_detected'):
                            st.write("**Issues Detected:**")
                            for issue in ai_response['issues_detected']:
                                st.write(f"- {issue}")
                        if ai_response.get('manual_fix_required'):
                            st.info(f"**Manual Fix Required:** {ai_response['manual_fix_required']}")
                
                # 6. Report Generation
                report_path = generate_markdown_report(
                    uploaded_file.name, actual_source, target_dialect, status, 
                    sql_content, final_translated_sql, ai_response
                )
                json_path = generate_issues_json(uploaded_file.name, ai_response)
                
                # 7. Database Logging
                log_migration(uploaded_file.name, actual_source, target_dialect, status, issues)
                
                # Save translated SQL to disk and Show File Paths instead of download buttons to prevent browser crashes
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                
                translated_sql_path = os.path.join(OUTPUT_DIR, f"translated_{uploaded_file.name}")
                with open(translated_sql_path, "w", encoding="utf-8") as f:
                    f.write(final_translated_sql)
                    
                st.success("✅ Migration completed successfully! Files have been saved locally to avoid browser memory limits.")
                st.markdown("### 📁 Output Files Saved To:")
                st.code(f"Translated SQL: {translated_sql_path}\nReport: {report_path if report_path else 'None'}\nIssues JSON: {json_path if json_path else 'None'}")

elif page == "Migration History":
    st.title("📊 Migration Dashboard")
    
    col_title, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("🗑️ Clear History", use_container_width=True):
            clear_history()
            st.rerun()
            
    history = get_history(limit=20)
    df = pd.DataFrame(history)
    
    if df.empty:
        st.info("No migrations have been run yet.")
    else:
        # Dashboard metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Recent Files", len(df))
        col2.metric("Successful", len(df[df['status'] == 'SUCCESS']))
        col3.metric("Failed", len(df[df['status'] == 'FAILED']))
        col4.metric("Partial/Manual", len(df[df['status'] == 'PARTIAL']))
        
        st.markdown("### Recent Migrations (Last 20)")
        st.dataframe(
            df[['timestamp', 'filename', 'source_database', 'target_database', 'status']], 
            use_container_width=True
        )
        
        # Optionally show issues for a selected migration
        st.markdown("### Migration Details")
        selected_id = st.selectbox("Select Migration ID to view issues", df['id'].tolist())
        selected_row = df[df['id'] == selected_id].iloc[0]
        
        issues = json.loads(selected_row['issues']) if selected_row['issues'] else []
        if issues:
            st.warning("Issues Found:")
            for issue in issues:
                st.write(f"- {issue}")
        else:
            st.success("No issues recorded for this migration.")
