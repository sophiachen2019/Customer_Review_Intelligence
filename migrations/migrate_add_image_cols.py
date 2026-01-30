import db_utils
import psycopg2

def migrate_add_image_cols():
    print("Starting add image columns migration...")
    conn = db_utils.get_db_connection()
    try:
        cur = conn.cursor()
        
        cols = [
            ("image_path", "TEXT"),
            ("source_filename", "TEXT")
        ]
        
        for col_name, col_type in cols:
            try:
                print(f"Adding column {col_name}...")
                cur.execute(f"ALTER TABLE reviews ADD COLUMN IF NOT EXISTS {col_name} {col_type};")
            except Exception as e:
                print(f"Error adding {col_name}: {e}")
                conn.rollback()
        
        conn.commit()
        cur.close()
        print("Add image columns migration complete!")
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

    migrate_add_image_cols()
