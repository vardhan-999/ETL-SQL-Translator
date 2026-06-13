import os

def read_sql_file(file_path: str) -> str:
    """Read the contents of a SQL file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_streamlit_upload(uploaded_file) -> str:
    """Read content from a Streamlit UploadedFile object."""
    if uploaded_file is not None:
        return uploaded_file.getvalue().decode("utf-8")
    return ""
