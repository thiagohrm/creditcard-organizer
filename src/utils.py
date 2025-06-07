def read_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def write_csv(dataframe, file_path):
    dataframe.to_csv(file_path, index=False)

def filter_negative_transactions(transactions):
    return transactions[transactions['amount'] >= 0]