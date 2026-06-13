import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

def generate_markdown_report(filename: str, source: str, target: str, status: str, original_sql: str, translated_sql: str, ai_response: dict, output_dir: str = DEFAULT_OUTPUT_DIR):
    """Generate a markdown report of the migration."""
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f'migration_report_{filename}.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Migration Report: {filename}\n\n")
        f.write(f"**Source Dialect:** {source}\n")
        f.write(f"**Target Dialect:** {target}\n")
        f.write(f"**Status:** {status}\n\n")
        
        f.write("## Original SQL\n```sql\n")
        f.write(original_sql)
        f.write("\n```\n\n")
        
        f.write("## Translated SQL\n```sql\n")
        f.write(translated_sql)
        f.write("\n```\n\n")
        
        if ai_response:
            f.write("## AI Assessment\n")
            f.write(f"**Confidence Score:** {ai_response.get('confidence_score', 'N/A')}\n\n")
            f.write(f"### Explanation\n{ai_response.get('explanation', 'None')}\n\n")
            
            issues = ai_response.get('issues_detected', [])
            if issues:
                f.write("### Issues Detected\n")
                for issue in issues:
                    f.write(f"- {issue}\n")
                f.write("\n")
                
            manual_fix = ai_response.get('manual_fix_required', '')
            if manual_fix:
                f.write("### Manual Fixes Required\n")
                f.write(f"{manual_fix}\n")

    return report_path

def generate_issues_json(filename: str, ai_response: dict, output_dir: str = DEFAULT_OUTPUT_DIR):
    """Save issues detected by AI to a JSON file."""
    if not ai_response:
        return None
        
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, f'unresolved_issues_{filename}.json')
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(ai_response, f, indent=4)
        
    return json_path
