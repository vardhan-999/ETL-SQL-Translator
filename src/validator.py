import sqlglot

def validate_sql(sql_content: str, target_dialect: str) -> tuple[str, str]:
    """
    Validates translated SQL syntax by parsing it with SQLGlot's target dialect parser.
    Returns:
        tuple: (status, message) where status is "VALID" or "FAILED".
    """
    if not sql_content.strip():
        return "FAILED", "SQL content is empty."
        
    try:
        # Attempt to parse the whole script
        sqlglot.parse(sql_content, read=target_dialect)
        return "VALID", "Syntax is valid for target dialect."
    except sqlglot.errors.ParseError as e:
        return "FAILED", f"Syntax Error in Translated SQL: {str(e)}"
    except Exception as e:
        return "FAILED", f"Validation Error: {str(e)}"
