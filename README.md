# Credit Card Organizer

This project is designed to help users organize their credit card transactions by categorizing them into predefined categories such as restaurants, market, health, taxes, automotive, and online services. The application reads a CSV file containing transaction data, filters out negative amounts, and outputs a new CSV file with organized transactions.

## Project Structure

```
creditcard-organizer
├── src
│   ├── main.py            # Entry point of the application
│   ├── categorizer.py     # Contains the TransactionCategorizer class
│   ├── utils.py           # Utility functions for CSV handling
│   └── categories
│       └── __init__.py    # Initializer for the categories module
├── requirements.txt       # Lists project dependencies
└── README.md              # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd creditcard-organizer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command in your terminal:

```
python src/main.py <input_csv_file> <output_csv_file>
```

- `<input_csv_file>`: Path to the input CSV file containing the credit card transactions.
- `<output_csv_file>`: Path where the organized transactions will be saved.

## Example

### Input CSV Format

```
date,title,amount
2025-05-01,Restaurant A,50.00
2025-05-02,Market B,30.00
2025-05-03,Health Service C,-20.00
```

### Output CSV Format

```
date,title,amount,category
2025-05-01,Restaurant A,50.00,restaurants
2025-05-02,Market B,30.00,market
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.