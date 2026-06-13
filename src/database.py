import sqlite3
import os
import json
from datetime import datetime

# Resolve the path to be inside the backend folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, 'migration_history.db')

def get_connection():
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS migration_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            source_database TEXT NOT NULL,
            target_database TEXT NOT NULL,
            status TEXT NOT NULL,
            issues TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_migration(filename: str, source: str, target: str, status: str, issues: list = None):
    """Log a migration attempt to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    issues_json = json.dumps(issues) if issues else "[]"
    
    cursor.execute('''
        INSERT INTO migration_history (filename, source_database, target_database, status, issues, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (filename, source, target, status, issues_json, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_history(limit: int = 20):
    """Retrieve migration history, limited to the most recent entries."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM migration_history ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_history():
    """Clear all records from the migration history table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM migration_history')
    conn.commit()
    conn.close()

# Initialize db when module is imported
init_db()
