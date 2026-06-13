import json
import urllib.request
import urllib.error
import os

def get_llm_translation_and_issues(original_sql: str, source: str, target: str, error_msg: str = "") -> dict:
    """
    Sends the SQL and any parser error to a local Ollama LLM to get a structured JSON response
    with translation, issues, and manual fixes.
    """
    prompt = f"""
    You are an expert database migration engineer.
    Analyze the following SQL migration from {source} to {target}.
    
    Original SQL:
    ```sql
    {original_sql}
    ```
    
    Parser Error context (if any): {error_msg}
    
    Provide the most accurate translation possible. If there are syntax or features that are completely 
    unsupported in the target dialect, note them in the issues and manual fixes sections.

    Return ONLY JSON in the following structure:
    {{
    "translated_sql": "<the fully translated SQL string>",
    "issues_detected": ["<issue 1>", "<issue 2>"],
    "manual_fix_required": "<description of what a human needs to do manually, or empty if none>",
    "confidence_score": "<e.g., 90%>",
    "explanation": "<brief explanation of the changes made>"
    }}
    """

    # Ollama endpoint
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3", # You can change this to 'mistral' or another model you have installed
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        # Parse the JSON response from Ollama
        try:
            return json.loads(result['response'])
        except json.JSONDecodeError:
            return {
                "translated_sql": "",
                "issues_detected": ["LLM returned malformed JSON."],
                "manual_fix_required": result['response'],
                "confidence_score": "0%",
                "explanation": "Failed to parse LLM response."
            }
            
    except Exception as e:
        return {
            "translated_sql": "",
            "issues_detected": [f"Ollama API Error: {str(e)}"],
            "manual_fix_required": "Ensure Ollama is running locally and the model (e.g., `ollama run llama3`) is installed.",
            "confidence_score": "0%",
            "explanation": "LLM agent failed to connect to Ollama."
        }
