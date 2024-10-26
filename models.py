from datetime import datetime
from database import get_db_connection
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT * FROM users WHERE username = %s
        """, (username,))
        
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    
    @staticmethod
    def authenticate(username, password):
        user = User.get_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            return user
        return None
    
    @staticmethod
    def create_user(username, password, role='guest'):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (username, generate_password_hash(password), role))
            
            user = cur.fetchone()
            conn.commit()
            return user
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

class ShippingEntry:
    @staticmethod
    def add_entry(date, project_name, description, category, status, user_id=None):
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                INSERT INTO shipping_entries (date, project_name, description, category, status, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (date, project_name, description, category, status, user_id))
            
            entry_id = cur.fetchone()[0]
            conn.commit()
            return entry_id
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_entries(user_id=None):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get all public entries and user-specific entries if authenticated
            cur.execute("""
                SELECT id, date::date as date, project_name, description, 
                       category, status, created_at 
                FROM shipping_entries
                ORDER BY date DESC
            """)
            
            entries = cur.fetchall()
            return entries
        finally:
            cur.close()
            conn.close()

class Achievement:
    @staticmethod
    def init_achievements():
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create achievements table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                badge_icon TEXT,
                unlocked_at TIMESTAMP DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER
            )
        """)
        
        # Insert default achievements if they don't exist
        default_achievements = [
            ("Starter Ship", "Ship your first project", "🌟"),
            ("Weekly Warrior", "Complete 7 days shipping streak", "🔥"),
            ("Monthly Master", "Complete 30 days shipping streak", "👑"),
            ("Category Collector", "Ship projects in all categories", "🎯"),
            ("Speed Demon", "Ship 3 projects in a single day", "⚡"),
        ]
        
        for achievement in default_achievements:
            cur.execute("""
                INSERT INTO achievements (name, description, badge_icon)
                SELECT %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM achievements WHERE name = %s
                )
            """, (*achievement, achievement[0]))
        
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_achievements(user_id=None):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        if user_id:
            cur.execute("""
                SELECT * FROM achievements
                WHERE user_id = %s OR user_id IS NULL
                ORDER BY unlocked_at NULLS LAST, name
            """, (user_id,))
        else:
            cur.execute("""
                SELECT * FROM achievements
                ORDER BY unlocked_at NULLS LAST, name
            """)
        
        achievements = cur.fetchall()
        cur.close()
        conn.close()
        return achievements

    @staticmethod
    def unlock_achievement(name, user_id=None):
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                UPDATE achievements
                SET unlocked_at = CURRENT_TIMESTAMP, user_id = %s
                WHERE name = %s AND unlocked_at IS NULL
                RETURNING id
            """, (user_id, name))
            
            unlocked = cur.fetchone() is not None
            conn.commit()
            return unlocked
        finally:
            cur.close()
            conn.close()
