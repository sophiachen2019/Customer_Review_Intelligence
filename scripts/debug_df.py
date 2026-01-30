import db_utils
import pandas as pd

try:
    df = db_utils.get_all_reviews()
    print("Columns:", df.columns.tolist())
    if 'review_date' in df.columns:
        print("Review Date Head:")
        print(df['review_date'].head())
        print("Review Date Type:", df['review_date'].dtype)
        print("First value type:", type(df['review_date'].iloc[0]) if not df.empty else "Empty")
    else:
        print("review_date column NOT found!")
except Exception as e:
    print(f"Error: {e}")
