import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

def connect_to_supabase():
    """
    Connect to Supabase PostgreSQL database using credentials from .env file.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            port=os.getenv("PORT"),
            sslmode=os.getenv("SSLMODE")
        )
        print("Connection to Supabase successful")
        return conn
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None
    
if __name__ == "__main__":
    connect_to_supabase()
    