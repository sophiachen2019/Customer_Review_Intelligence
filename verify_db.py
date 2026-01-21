import db_utils
import streamlit as st
import os

# Mock secrets loading for standalone run
try:
    import toml
    secrets = toml.load(".streamlit/secrets.toml")
    # Inject into os.environ so db_utils can pick it up if st.secrets fails
    os.environ["NEON_DB_CONNECTION_STRING"] = secrets["NEON_DB_CONNECTION_STRING"]
except Exception as e:
    print(f"Could not load secrets: {e}")

print("Testing Database Connection...")
try:
    conn = db_utils.get_db_connection()
    print("Connection successful!")
    
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("Query executed successfully.")
    
    cur.close()
    conn.close()
    print("Connection closed.")
except Exception as e:
    print(f"Database connection failed: {e}")
