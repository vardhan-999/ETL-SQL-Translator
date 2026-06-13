import sqlglot
from sqlglot import parse_one, errors

def detect_dialect(sql_content: str) -> str:
    """
    Attempt to detect the SQL dialect using sqlglot's parsers.
    It tries common dialects and returns the first one that successfully parses.
    Note: This is a heuristic and might not be 100% accurate for complex mixed queries.
    """
    dialects_to_try = ['mysql', 'postgres', 'sqlite', 'oracle', 'sqlserver', 'snowflake']
    
    for dialect in dialects_to_try:
        try:
            # Try to parse the first statement
            parse_one(sql_content, read=dialect)
            return dialect
        except errors.ParseError:
            continue
    
    return "unknown"
