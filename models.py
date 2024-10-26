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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    def get_achievements():
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT * FROM achievements
            ORDER BY unlocked_at NULLS LAST, name
        """)
        
        achievements = cur.fetchall()
        cur.close()
        conn.close()
        return achievements

    @staticmethod
    def unlock_achievement(name):
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE achievements
            SET unlocked_at = CURRENT_TIMESTAMP
            WHERE name = %s AND unlocked_at IS NULL
            RETURNING id
        """, (name,))
        
        unlocked = cur.fetchone() is not None
        conn.commit()
        cur.close()
        conn.close()
        return unlocked
