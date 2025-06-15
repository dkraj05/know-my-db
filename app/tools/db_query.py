import psycopg2
import pandas as pd
import os
from typing import Dict, Any
import re

def get_db_connection():
    """Create and return a database connection."""
    return psycopg2.connect(
        host=os.getenv('PG_HOST', 'localhost'),
        port=os.getenv('PG_PORT', '5432'),
        user=os.getenv('PG_USER', 'postgres'),
        password=os.getenv('PG_PASS', 'postgres'),
        database=os.getenv('PG_DB', 'knowmydb')
    )

def is_safe_query(sql: str) -> bool:
    """Check if the SQL query is safe (only SELECT statements)."""
    # Remove comments and normalize whitespace
    sql_clean = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
    sql_clean = re.sub(r'/\*.*?\*/', '', sql_clean, flags=re.DOTALL)
    sql_clean = sql_clean.strip().upper()
    
    # Check if it starts with SELECT
    if not sql_clean.startswith('SELECT'):
        return False
    
    # Check for dangerous keywords
    dangerous_keywords = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 
        'TRUNCATE', 'GRANT', 'REVOKE', 'EXEC', 'EXECUTE'
    ]
    
    for keyword in dangerous_keywords:
        if keyword in sql_clean:
            return False
    
    return True

def run_query(sql: str) -> Dict[str, Any]:
    """
    Execute a SQL query and return results.
    Only SELECT queries are allowed for security.
    Results are limited to 5 rows to prevent large data exposure.
    """
    try:
        # Validate query safety
        if not is_safe_query(sql):
            return {
                "success": False,
                "error": "Only SELECT queries are allowed for security reasons.",
                "data": None
            }
        
        # Add LIMIT if not present
        sql_upper = sql.upper().strip()
        if 'LIMIT' not in sql_upper:
            sql += ' LIMIT 5'
        
        # Execute query
        conn = get_db_connection()
        df = pd.read_sql_query(sql, conn)
        conn.close()
        
        # Convert to dictionary format
        result_data = df.to_dict('records')
        
        return {
            "success": True,
            "error": None,
            "data": result_data,
            "row_count": len(result_data),
            "columns": list(df.columns)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        } 