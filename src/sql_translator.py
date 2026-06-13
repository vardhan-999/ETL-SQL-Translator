import sqlglot
from sqlglot import errors

def translate_sql(sql_content: str, source_dialect: str, target_dialect: str) -> tuple[str, bool, str]:
    """
    Translates SQL using SQLGlot.
    Returns:
        tuple: (translated_sql, is_successful, error_message)
    """
    try:
        # We parse the full script, not just one statement.
        # However, sqlglot transpiles a list of statements.
        statements = sqlglot.parse(sql_content, read=source_dialect)
        
        translated_statements = []
        for stmt in statements:
            if stmt:
                translated_statements.append(stmt.sql(dialect=target_dialect))
                
        # Join statements with a semicolon and a newline
        translated_sql = ";\n\n".join(translated_statements)
        if translated_sql:
            translated_sql += ";"
            
        return translated_sql, True, ""
        
    except errors.ParseError as e:
        return "", False, f"SQLGlot Parse Error: {str(e)}"
    except errors.UnsupportedError as e:
        return "", False, f"SQLGlot Unsupported Feature Error: {str(e)}"
    except Exception as e:
        return "", False, f"Unexpected Translation Error: {str(e)}"
