import os
from database import get_db_connection
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def update_project(project_id, updates):
    """
    Update a project's details in the shipping_entries table
    
    Args:
        project_id (int): The ID of the project to update
        updates (dict): Dictionary containing the fields to update and their new values
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Build the SET clause dynamically based on the provided updates
        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values())
        values.append(project_id)  # Add project_id for WHERE clause
        
        query = f"""
            UPDATE shipping_entries 
            SET {set_clause}
            WHERE id = %s
        """
        
        cur.execute(query, values)
        conn.commit()
        print(f"Successfully updated project {project_id}")
        
    except Exception as e:
        print(f"Error updating project: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    updates = {
        "project_name": "cookie.bchwy.com",
    }
    update_project(4, updates)