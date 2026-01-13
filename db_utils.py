import psycopg2
import streamlit as st
import os
import pandas as pd

def get_db_connection():
    """Establishes a connection to the Neon Postgres database."""
    try:
        # Try getting from Streamlit secrets first
        dsn = st.secrets["NEON_DB_CONNECTION_STRING"]
        conn = psycopg2.connect(dsn)
        return conn
    except (FileNotFoundError, KeyError):
        # Fallback to environment variable
        dsn = os.getenv("NEON_DB_CONNECTION_STRING")
        if dsn:
            conn = psycopg2.connect(dsn)
            return conn
        else:
            raise ValueError("Database connection string not found.")

def init_db():
    """Initializes the database with the schema."""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        with open('schema.sql', 'r') as f:
            schema = f.read()
        cur.execute(schema)
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error initializing DB: {e}")
        conn.rollback()
    finally:
        conn.close()

def check_duplicate(user_name, content):
    """Checks if a review already exists to prevent duplicates."""
    conn = get_db_connection()
    exists = False
    try:
        cur = conn.cursor()
        query = "SELECT id FROM reviews WHERE user_name = %s AND content = %s"
        cur.execute(query, (user_name, content))
        if cur.fetchone():
            exists = True
        cur.close()
    except Exception as e:
        print(f"Error checking duplicate: {e}")
    finally:
        conn.close()
    return exists

def insert_review(data):
    """Inserts a new review into the database."""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # review_id and review_year have defaults, so we don't need to insert them explicitly unless we want to override.
        query = """
            INSERT INTO reviews (user_name, review_date, rating_overall, rating_taste, rating_env, rating_service, rating_value, content, image_path, source_filename)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Handle date parsing or cleaning if necessary in app.py before calling this
        cur.execute(query, (
            data.get('user_name'), 
            data.get('review_date'), 
            data.get('rating_overall'),
            data.get('rating_taste'),
            data.get('rating_env'),
            data.get('rating_service'),
            data.get('rating_value'),
            data.get('content'),
            data.get('image_path'),
            data.get('source_filename')
        ))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error inserting review: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()



@st.cache_data(ttl=300)
def get_all_reviews():
    """Fetches all reviews for the dashboard."""
    conn = get_db_connection()
    try:
        query = "SELECT * FROM reviews ORDER BY id DESC"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


