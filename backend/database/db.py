import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    """Returns a connection to the PostgreSQL database."""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def init_db():
    """Initializes the database schema."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Read the schema file and execute it
    try:
        with open('backend/database/schema.sql', 'r') as f:
            schema_script = f.read()
            cur.execute(schema_script)
            conn.commit()
            print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    # Initialize the database when run directly
    init_db()
