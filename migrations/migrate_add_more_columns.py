import db_utils
import psycopg2

def migrate_add_columns():
    print("Starting add columns migration...")
    conn = db_utils.get_db_connection()
    try:
        cur = conn.cursor()
        
        # Add review_year
        try:
            print("Adding column review_year...")
            cur.execute("ALTER TABLE reviews ADD COLUMN IF NOT EXISTS review_year INTEGER DEFAULT 2025;")
        except Exception as e:
            print(f"Error adding review_year: {e}")
            conn.rollback()

        # Add review_id
        # Note: Adding a SERIAL column to an existing table automatically populates it.
        try:
            print("Adding column review_id...")
            # Check if column exists first to avoid error on retry if SERIAL logic is tricky with IF NOT EXISTS
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='reviews' AND column_name='review_id';")
            if not cur.fetchone():
                cur.execute("ALTER TABLE reviews ADD COLUMN review_id SERIAL;")
            else:
                print("Column review_id already exists.")
        except Exception as e:
            print(f"Error adding review_id: {e}")
            conn.rollback()
        
        conn.commit()
        cur.close()
        print("Add columns migration complete!")
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    # Mock secrets loading
    import os
    try:
        import toml
        secrets = toml.load(".streamlit/secrets.toml")
        os.environ["NEON_DB_CONNECTION_STRING"] = secrets["NEON_DB_CONNECTION_STRING"]
    except Exception as e:
        print(f"Could not load secrets: {e}")

    migrate_add_columns()
