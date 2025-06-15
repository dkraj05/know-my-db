import psycopg2
import os
from typing import Dict, Any, List

def get_db_connection():
    """Create and return a database connection."""
    return psycopg2.connect(
        host=os.getenv('PG_HOST', 'localhost'),
        port=os.getenv('PG_PORT', '5432'),
        user=os.getenv('PG_USER', 'postgres'),
        password=os.getenv('PG_PASS', 'password'),
        database=os.getenv('PG_DB', 'knowmydb')
    )

def get_table_names() -> Dict[str, Any]:
    """
    Get all table names from the database.
    Returns a list of table names in the current database.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query to get all table names from the public schema
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """
        
        cursor.execute(query)
        tables = cursor.fetchall()
        
        # Extract table names from tuples
        table_names = [table[0] for table in tables]
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "error": None,
            "tables": table_names,
            "count": len(table_names)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "tables": None,
            "count": 0
        } 