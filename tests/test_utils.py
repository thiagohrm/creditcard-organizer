import pandas as pd
from src.utils import read_csv, write_csv, filter_negative_transactions

def test_filter_negative_transactions(tmp_path):
    df = pd.DataFrame([
        {"date": "2025-01-01", "title": "A", "amount": 10},
        {"date": "2025-01-02", "title": "B", "amount": -5},
    ])
    filtered = filter_negative_transactions(df)
    assert len(filtered) == 1
    assert filtered.iloc[0]['amount'] == 10

def test_read_write_csv(tmp_path):
    df = pd.DataFrame([
        {"date": "2025-01-01", "title": "A", "amount": 10},
    ])
    file = tmp_path / "test.csv"
    write_csv(df, file)
    df2 = read_csv(file)
    assert df2.equals(df)