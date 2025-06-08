import pandas as pd
from utils import read_csv, write_csv, filter_negative_transactions, generate_pdf, merge_installments

def test_filter_negative_transactions():
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

def test_generate_pdf_runs(tmp_path):
    df = pd.DataFrame([
        {"date": "2025-01-01", "title": "A", "amount": 10, "category": "market"},
        {"date": "2025-01-02", "title": "B", "amount": 20, "category": "market"},
    ])
    file = tmp_path / "test.pdf"
    generate_pdf(str(file), df)
    assert file.exists()

def test_merge_installments():
    df = pd.DataFrame([
        {"date": "2025-05-04", "title": "Store X Parcela 1/3", "amount": 100},
        {"date": "2025-06-04", "title": "Store X Parcela 2/3", "amount": 100},
        {"date": "2025-07-04", "title": "Store X Parcela 3/3", "amount": 100},
        {"date": "2025-05-01", "title": "Other Store", "amount": 50},
    ])
    merged = merge_installments(df)
    # Should have two rows: one for "Store X" (sum 300), one for "Other Store"
    assert len(merged) == 2
    assert any((merged['title'] == "Store X") & (merged['amount'] == 300))
    assert any((merged['title'] == "Other Store") & (merged['amount'] == 50))