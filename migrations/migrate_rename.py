import db_utils
import psycopg2

def migrate_rename():
    print("Starting column rename migration...")
    conn = db_utils.get_db_connection()
    try:
        cur = conn.cursor()
        
        renames = [
            ("username", "user_name"),
            ("rating", "rating_overall"),
            ("rating_environment", "rating_env")
        ]
        
        for old_col, new_col in renames:
            try:
                print(f"Renaming {old_col} to {new_col}...")
                cur.execute(f"ALTER TABLE reviews RENAME COLUMN {old_col} TO {new_col};")
            except Exception as e:
                print(f"Error renaming {old_col}: {e}")
                conn.rollback()
        
        conn.commit()
        cur.close()
        print("Rename migration complete!")
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

    migrate_rename()
