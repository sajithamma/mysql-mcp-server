from fastmcp import FastMCP
import sqlite3
from typing import List, Dict, Any

mcp = FastMCP('SQLite Database Manager')

def get_db_connection():
    return sqlite3.connect('sample.db')

@mcp.tool()
def list_tables() -> List[str]:
    """List all tables in the SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

@mcp.tool()
def describe_table(table_name: str) -> Dict[str, Any]:
    """Get the schema information for a specific table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get table info
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    # Get foreign key info
    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    foreign_keys = cursor.fetchall()
    
    # Format the response
    schema = {
        "table_name": table_name,
        "columns": [
            {
                "name": col[1],
                "type": col[2],
                "not_null": bool(col[3]),
                "default_value": col[4],
                "is_primary_key": bool(col[5])
            }
            for col in columns
        ],
        "foreign_keys": [
            {
                "id": fk[0],
                "seq": fk[1],
                "table": fk[2],
                "from": fk[3],
                "to": fk[4],
                "on_update": fk[5],
                "on_delete": fk[6],
                "match": fk[7]
            }
            for fk in foreign_keys
        ]
    }
    
    conn.close()
    return schema

@mcp.tool()
def run_query(query: str) -> Dict[str, Any]:
    """Execute a SQL query and return the results."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Execute the query
        cursor.execute(query)
        
        # Get column names
        columns = [description[0] for description in cursor.description] if cursor.description else []
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Convert results to list of dictionaries
        formatted_results = []
        for row in results:
            formatted_row = {}
            for i, value in enumerate(row):
                # Convert datetime objects to strings
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                formatted_row[columns[i]] = value
            formatted_results.append(formatted_row)
        
        response = {
            "success": True,
            "columns": columns,
            "results": formatted_results,
            "row_count": len(results)
        }
        
    except sqlite3.Error as e:
        response = {
            "success": False,
            "error": str(e)
        }
    
    conn.close()
    return response

if __name__ == '__main__':
    mcp.run()

# Run using: fastmcp run mysql-msp-server-sse.py:mcp --transport sse --host 127.0.0.1 --port 8000

    