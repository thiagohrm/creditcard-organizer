import pandas as pd
from categorizer import TransactionCategorizer

def test_categorize_title_default():
    categorizer = TransactionCategorizer()
    assert categorizer.categorize_title("Burger King") == "restaurants"
    assert categorizer.categorize_title("Geraldo Benedete e Cia") == "market"
    assert categorizer.categorize_title("Unknown Store") == "others"

def test_categorize_transactions_removes_negative():
    categorizer = TransactionCategorizer()
    df = pd.DataFrame([
        {"date": "2025-01-01", "title": "Burger King", "amount": 50},
        {"date": "2025-01-02", "title": "Burger King", "amount": -10},
    ])
    result = categorizer.categorize_transactions(df)
    assert len(result) == 1
    assert result.iloc[0]['category'] == "restaurants"