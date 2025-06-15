import psycopg2
import pandas as pd
import os
from typing import Dict, Any

def get_db_connection():
    """Create and return a database connection."""
    return psycopg2.connect(
        host=os.getenv('PG_HOST', 'localhost'),
        port=os.getenv('PG_PORT', '5432'),
        user=os.getenv('PG_USER', 'postgres'),
        password=os.getenv('PG_PASS', 'password'),
        database=os.getenv('PG_DB', 'knowmydb')
    )

def summarize_table(table_name: str) -> Dict[str, Any]:
    """
    Get table schema information and sample data.
    Returns table structure, column info, and first 3 rows.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get table schema information
        schema_query = """
        SELECT 
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns 
        WHERE table_name = %s 
        AND table_schema = 'public'
        ORDER BY ordinal_position;
        """
        
        cursor.execute(schema_query, (table_name,))
        schema_info = cursor.fetchall()
        
        if not schema_info:
            return {
                "success": False,
                "error": f"Table '{table_name}' not found.",
                "schema": None,
                "sample_data": None,
                "row_count": 0
            }
        
        # Format schema information
        columns = []
        for col in schema_info:
            columns.append({
                "name": col[0],
                "type": col[1],
                "nullable": col[2] == 'YES',
                "default": col[3]
            })
        
        # Get row count
        count_query = f"SELECT COUNT(*) FROM {table_name};"
        cursor.execute(count_query)
        total_rows = cursor.fetchone()[0]
        
        # Get sample data (first 3 rows)
        sample_query = f"SELECT * FROM {table_name} LIMIT 3;"
        df_sample = pd.read_sql_query(sample_query, conn)
        sample_data = df_sample.to_dict('records')
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "error": None,
            "table_name": table_name,
            "schema": columns,
            "sample_data": sample_data,
            "total_rows": total_rows,
            "sample_rows": len(sample_data)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "schema": None,
            "sample_data": None,
            "row_count": 0
        } 