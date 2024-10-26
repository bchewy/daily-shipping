import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['PGHOST'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT']
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create shipping_entries table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shipping_entries (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            project_name VARCHAR(255) NOT NULL,
            description TEXT,
            category VARCHAR(100),
            status VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    
    # Initialize achievements
    from models import Achievement
    Achievement.init_achievements()
