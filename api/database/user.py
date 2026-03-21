import os
import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5433'),
        database=os.getenv('DB_NAME', 'taskdb'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres123')
    )

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    # Ensure hashed is a string
    if isinstance(hashed, (bytes, memoryview)):
        hashed = hashed.decode('utf-8')
    elif isinstance(hashed, tuple):
        hashed = hashed[0] if hashed else ''
    
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(username: str, email: str, password: str, full_name: str = None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute(
            "SELECT id FROM users WHERE username = %s OR email = %s",
            (username, email)
        )
        existing = cur.fetchone()
        
        if existing:
            return None, "Username or email already exists"
        
        password_hash = hash_password(password)
        
        cur.execute(
            """INSERT INTO users (username, email, password_hash, full_name) 
               VALUES (%s, %s, %s, %s) RETURNING id, username, email, full_name""",
            (username, email, password_hash, full_name)
        )
        
        user = cur.fetchone()
        conn.commit()
        return user, "User created successfully"
        
    except Exception as e:
        conn.rollback()
        return None, f"Error: {str(e)}"
    finally:
        cur.close()
        conn.close()
        
def login_user(username_or_email: str, password: str):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute(
            """SELECT id, username, email, password_hash, full_name, is_active 
               FROM users 
               WHERE username = %s OR email = %s""",
            (username_or_email, username_or_email)
        )
        
        user = cur.fetchone()
        
        if not user:
            return None, "Invalid credentials"
        
        if not user['is_active']:
            return None, "Account is deactivated"
        
        # Convert password_hash to string if needed
        password_hash = user['password_hash']
        if isinstance(password_hash, (bytes, memoryview)):
            password_hash = password_hash.decode('utf-8')
        elif isinstance(password_hash, tuple):
            password_hash = password_hash[0] if password_hash else ''
        
        if not verify_password(password, password_hash):
            return None, "Invalid credentials"
        
        # Remove password_hash from response
        user_dict = dict(user)
        del user_dict['password_hash']
        return user_dict, "Login successful"
        
    except Exception as e:
        return None, f"Error: {str(e)}"
    finally:
        cur.close()
        conn.close()