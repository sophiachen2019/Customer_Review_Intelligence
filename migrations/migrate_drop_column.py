import db_utils
import psycopg2

def migrate_drop_review_id():
    print("Starting drop review_id migration...")
    conn = db_utils.get_db_connection()
    try:
        cur = conn.cursor()
        try:
            print("Dropping column review_id...")
            cur.execute("ALTER TABLE reviews DROP COLUMN IF EXISTS review_id;")
        except Exception as e:
            print(f"Error dropping review_id: {e}")
            conn.rollback()
        
        conn.commit()
        cur.close()
        print("Drop migration complete!")
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
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

    migrate_drop_review_id()
