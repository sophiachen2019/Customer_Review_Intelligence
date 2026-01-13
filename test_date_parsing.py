import pandas as pd
import datetime

def test_date(raw_date):
    print(f"Testing date: {raw_date}")
    try:
        parsed_date = pd.to_datetime(raw_date).strftime('%Y-%m-%d')
        print(f"Parsed: {parsed_date}")
    except:
        fallback = datetime.date.today().strftime('%Y-%m-%d')
        print(f"Failed. Fallback: {fallback}")

test_date("12/30")
test_date("12-30")
test_date("2025-12-30")
test_date("12/30/2024")
