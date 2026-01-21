import db_utils
import psycopg2

def migrate():
    print("Starting migration...")
    conn = db_utils.get_db_connection()
    try:
        cur = conn.cursor()
        
        # Add new columns if they don't exist
        columns = [
            ("rating_taste", "FLOAT"),
            ("rating_environment", "FLOAT"),
            ("rating_service", "FLOAT"),
            ("rating_value", "FLOAT")
        ]
        
        for col_name, col_type in columns:
            try:
                print(f"Adding column {col_name}...")
                cur.execute(f"ALTER TABLE reviews ADD COLUMN IF NOT EXISTS {col_name} {col_type};")
            except Exception as e:
                print(f"Error adding {col_name}: {e}")
                conn.rollback()
        
        # Change rating type to FLOAT
        try:
            print("Altering rating column type to FLOAT...")
            cur.execute("ALTER TABLE reviews ALTER COLUMN rating TYPE FLOAT;")
        except Exception as e:
            print(f"Error altering rating column: {e}")
            conn.rollback()

        conn.commit()
        cur.close()
        print("Migration complete!")
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    # Mock secrets loading for standalone run if needed, similar to verify_db.py
    import os
    try:
        import toml
        secrets = toml.load(".streamlit/secrets.toml")
        os.environ["NEON_DB_CONNECTION_STRING"] = secrets["NEON_DB_CONNECTION_STRING"]
    except Exception as e:
        print(f"Could not load secrets from file (might rely on env vars): {e}")

    migrate()
