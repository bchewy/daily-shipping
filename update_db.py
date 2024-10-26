import os
from database import get_db_connection
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def update_admin_and_add_projects():
		conn = get_db_connection()
		cur = conn.cursor()

		# 1. Update admin password
		# new_password = "223GWyHNa4gF3c"  # Replace with your desired password
		# cur.execute("""
		# 		UPDATE users 
		# 		SET password_hash = %s 
		# 		WHERE username = 'admin'
		# """, (generate_password_hash(new_password),))

		# 2. Add sample completed projects
		completed_projects = [
				# {
				# 		"date": datetime.now() - timedelta(days=3),
				# 		"project_name": "when2meet.bchwy.com",
				# 		"description": "Allow for easier lazy-using for when2meet.com",
				# 		"category": "Web Development",
				# 		"status": "Completed"
				# },
				# {
				# 		"date": datetime.now() - timedelta(days=2),
				# 		"project_name": "bchewy.com",
				# 		"description": "Updated our portfolio website",
				# 		"category": "Web Development",
				# 		"status": "Completed"
				# },
				{
						"date": datetime.now() - timedelta(days=1),
						"project_name": "cookib.bchwy.com",
						"description": "Bash Cookie Clicker Game",
						"category": "Game/Web Dev",
						"status": "Completed"
				},
		]

		for project in completed_projects:
				cur.execute("""
						INSERT INTO shipping_entries 
						(date, project_name, description, category, status)
						VALUES (%s, %s, %s, %s, %s)
				""", (
						project["date"],
						project["project_name"],
						project["description"],
						project["category"],
						project["status"]
				))

		conn.commit()
		cur.close()
		conn.close()


# Run the function
if __name__ == "__main__":
		update_admin_and_add_projects()