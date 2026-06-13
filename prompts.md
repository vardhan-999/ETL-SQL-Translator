# LLM Prompts

## 1. SQL Translation & Issue Detection

**System/Role Prompt:**
You are an expert database migration engineer.

**User Prompt:**
Analyze the following SQL migration from `{source}` to `{target}`.

Original SQL:
```sql
{original_sql}
```

Parser Error context (if any): `{error_msg}`

Provide the most accurate translation possible. If there are syntax or features that are completely 
unsupported in the target dialect, note them in the issues and manual fixes sections.

Return ONLY JSON in the following structure:
{
"translated_sql": "<the fully translated SQL string>",
"issues_detected": ["<issue 1>", "<issue 2>"],
"manual_fix_required": "<description of what a human needs to do manually, or empty if none>",
"confidence_score": "<e.g., 90%>",
"explanation": "<brief explanation of the changes made>"
}

---

## Example Expected Output

```json
{
  "translated_sql": "CREATE TABLE employee(\n    id SERIAL PRIMARY KEY,\n    name VARCHAR(50),\n    created TIMESTAMP\n);",
  "issues_detected": [
    "MySQL AUTO_INCREMENT mapped to PostgreSQL SERIAL",
    "MySQL DATETIME mapped to PostgreSQL TIMESTAMP"
  ],
  "manual_fix_required": "",
  "confidence_score": "100%",
  "explanation": "Converted auto-incrementing ID to SERIAL and updated datetime field to TIMESTAMP."
}
```
