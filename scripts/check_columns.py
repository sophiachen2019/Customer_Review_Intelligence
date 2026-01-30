import db_utils
import psycopg2

def check_columns():
    print("Checking columns in reviews table...")
    conn = db_utils.get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='reviews';")
        cols = cur.fetchall()
        print("Columns found:")
        for col in cols:
            print(f"- {col[0]}")
        cur.close()
    except Exception as e:
        print(f"Error checking columns: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import os
    try:
        import toml
        secrets = toml.load(".streamlit/secrets.toml")
        os.environ["NEON_DB_CONNECTION_STRING"] = secrets["NEON_DB_CONNECTION_STRING"]
    except Exception as e:
        print(f"Could not load secrets: {e}")

    check_columns()
