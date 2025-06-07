import pandas as pd
import argparse
from categorizer import TransactionCategorizer
from utils import read_csv, write_csv

def main():
    parser = argparse.ArgumentParser(description='Organize credit card transactions by category.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file containing transactions.')
    parser.add_argument('output_file', type=str, help='Path to the output CSV file for organized transactions.')
    
    args = parser.parse_args()
    
    # Read transactions from the input CSV file
    transactions = read_csv(args.input_file)
    
    # Create an instance of TransactionCategorizer
    categorizer = TransactionCategorizer()
    
    # Categorize transactions
    categorized_transactions = categorizer.categorize_transactions(transactions)
    
    # Write the organized transactions to the output CSV file
    write_csv(categorized_transactions, args.output_file)

if __name__ == '__main__':
    main()