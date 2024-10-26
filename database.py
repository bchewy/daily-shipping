import os
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER
        )
    """)

    # Create users table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'guest',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create default admin user if it doesn't exist
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')  # Default password if not set
    cur.execute("""
        INSERT INTO users (username, password_hash, role)
        SELECT 'admin', %s, 'admin'
        WHERE NOT EXISTS (
            SELECT 1 FROM users WHERE username = 'admin'
        )
    """, (generate_password_hash(admin_password),))
    
    conn.commit()
    cur.close()
    conn.close()
    
    # Initialize achievements
    from models import Achievement
    Achievement.init_achievements()
