from datetime import datetime
from database import get_db_connection
from psycopg2.extras import RealDictCursor

class ShippingEntry:
    @staticmethod
    def add_entry(date, project_name, description, category, status):
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO shipping_entries (date, project_name, description, category, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (date, project_name, description, category, status))
        
        entry_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return entry_id

    @staticmethod
    def get_all_entries():
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT id, date::date as date, project_name, description, category, status, created_at 
            FROM shipping_entries
            ORDER BY date DESC
        """)
        
        entries = cur.fetchall()
        cur.close()
        conn.close()
        return entries
