import pandas as pd
import argparse
from categorizer import TransactionCategorizer
from utils import read_csv, write_csv, generate_pdf
import os

def main():
    parser = argparse.ArgumentParser(description='Organize credit card transactions by category.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file containing transactions.')
    args = parser.parse_args()
    
    # Read transactions from the input CSV file
    transactions = read_csv(args.input_file)
    
    # Create an instance of TransactionCategorizer
    categorizer = TransactionCategorizer()
    
    # Categorize transactions
    categorized_transactions = categorizer.categorize_transactions(transactions)
    
    # Generate output file name
    base, ext = os.path.splitext(args.input_file)
    output_file = f"{base}-organized{ext}"
    
    # Write the organized transactions to the output CSV file
    write_csv(categorized_transactions, output_file)
    generate_pdf(args.input_file, categorized_transactions)

if __name__ == '__main__':
    main()