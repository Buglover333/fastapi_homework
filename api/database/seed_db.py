import os
import bcrypt
import psycopg2
from dotenv import load_dotenv
import sys

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5433'),
            database=os.getenv('DB_NAME', 'taskdb'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres123')
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}", file=sys.stderr)
        print(f"Attempted connection to: {os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5433')}", file=sys.stderr)
        raise

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def seed_database():
    conn = get_db_connection()
    cur = conn.cursor()
    
    test_users = [
        ("alice", "alice@example.com", "password123", "Alice Wonderland"),
        ("bob", "bob@example.com", "securepass", "Bob Builder"),
        ("charlie", "charlie@example.com", "mypassword", "Charlie Brown"),
        ("diana", "diana@example.com", "princess123", "Diana Prince"),
        ("eve", "eve@example.com", "evepass", "Eve Adams")
    ]
    
    try:
        for username, email, password, full_name in test_users:
            password_hash = hash_password(password)
            
            cur.execute(
                """INSERT INTO users (username, email, password_hash, full_name, is_active) 
                   VALUES (%s, %s, %s, %s, %s) 
                   ON CONFLICT (username) DO NOTHING""",
                (username, email, password_hash, full_name, True)
            )
        
        conn.commit()
        print(f"Successfully added {len(test_users)} test users")
        
        cur.execute("SELECT id, username, email, full_name FROM users")
        users = cur.fetchall()
        print("\nCurrent users in database:")
        for user in users:
            print(f"  - ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Name: {user[3]}")
            
    except Exception as e:
        conn.rollback()
        print(f"Error seeding database: {str(e)}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed_database()