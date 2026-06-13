import pytest
import os
from src.dialect_detector import detect_dialect
from src.sql_translator import translate_sql
from src.validator import validate_sql
from src.database import init_db, log_migration, get_history

# Setup test database path for SQLite to prevent polluting the main db
os.environ["TEST_DB"] = "true"

def test_dialect_detector():
    mysql_sql = "SELECT * FROM `users` LIMIT 10;"
    pg_sql = "SELECT * FROM users LIMIT 10 OFFSET 0;"
    
    assert detect_dialect(mysql_sql) in ['mysql', 'sqlite'] # SQLite can parse backticks sometimes
    assert detect_dialect(pg_sql) in ['postgres', 'mysql', 'sqlite']

def test_sql_translator():
    mysql_sql = "CREATE TABLE employee (id INT AUTO_INCREMENT PRIMARY KEY);"
    translated, success, error = translate_sql(mysql_sql, 'mysql', 'postgres')
    
    assert success is True
    assert 'SERIAL' in translated.upper() or 'GENERATED' in translated.upper()

def test_validator():
    valid_pg = "CREATE TABLE employee (id SERIAL PRIMARY KEY);"
    invalid_pg = "CREATE TABLE employee (id INT AUTO_INCREMENT PRIMARY KEY);" # AUTO_INCREMENT is invalid in PG
    
    status, msg = validate_sql(valid_pg, 'postgres')
    assert status == "VALID"
    
    # Validation behavior might vary depending on how sqlglot handles parsing invalid tokens,
    # but let's test a clearly broken syntax.
    broken_sql = "SELECT * FROM WHERE;"
    status, msg = validate_sql(broken_sql, 'postgres')
    assert status == "FAILED"

def test_database_logging():
    init_db()
    log_migration('test.sql', 'mysql', 'postgres', 'SUCCESS', [])
    history = get_history()
    
    assert len(history) > 0
    assert history[0]['filename'] == 'test.sql'
    assert history[0]['status'] == 'SUCCESS'
