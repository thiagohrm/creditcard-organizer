# Credit Card Organizer

This project helps users organize their credit card transactions by categorizing them into customizable categories (such as restaurants, market, health, taxes, automotive, online services, and more). The application reads one or more CSV files containing transaction data, filters out negative amounts, merges installment payments, and provides a graphical interface to view summaries, charts, and export reports.

## Project Structure

```
creditcard-organizer
├── src
│   ├── app_ui.py          # Main GUI application (entry point)
│   ├── categorizer.py     # Contains the TransactionCategorizer class
│   ├── utils.py           # Utility functions for CSV and PDF handling
│   ├── categories.json    # (Optional) Custom categories and keywords
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
python src/app_ui.py
```

This will launch the graphical user interface (GUI) for uploading your CSV(s), viewing charts, and exporting reports.

### Main Features

- **Multiple CSV Upload:** Select and analyze multiple CSV files at once.
- **Automatic Installment Merging:** Transactions with "Parcela X/Y" in the title are automatically merged and summed.
- **Summary Tab:** Pie chart and table summarizing spending by category.
- **Details Tab:** For each category, see a bar chart (by day or by month if multiple CSVs) and a table of transactions.
- **Amounts per Store Tab:** Pie chart and table showing total spent, transaction count, and mean amount for each store (top 30 stores shown individually, others grouped).
- **Store Drilldown:** Double-click a store in the Stores tab to see all transactions for that store.
- **Export to PDF:** Export all or selected categories to PDF.
- **Clean Data:** Remove all loaded data and reset the interface.

## Custom Categories

You can define your own categories and keywords by editing or creating a `categories.json` file in the `src` directory.  
Example format:

```json
{
    "market": ["benedete", "imperio", "market", "delta", "assai", "lojao", "americanas"],
    "health": ["drogal", "remedio", "saude", "raia", "drogasil", "pague menos", "ervanario"],
    "online services": ["netflix", "youtube", "google one", "ifood", "microsoft", "office", "apple", "melimais"],
    "restaurants": ["restaurante", "burger", "mcdonalds", "kissburgers", "lanchonete", "esfirraria", "churros", "real", "pandurata"],
    "automotive": ["posto", "nutag", "abastece", "abasteceai", "estacionamento", "f park"],
    "taxes": ["pagamento recebido", "txentregvisto"],
    "utilities": ["energia", "agua", "luz", "telefonia", "internet", "celular", "claro", "vivo", "oi", "tim"],
    "transportation": ["uber", "99", "cabify", "taxi", "transporte", "onibus", "metro", "trem"],
    "entertainment": ["cinema", "show", "teatro", "evento", "festival", "museu", "parque"],
    "clothing": ["roupa", "vestuario", "moda", "sapato", "calçado", "acessorios", "loja de roupas"],
    "electronics": ["eletronicos", "tecnologia", "celular", "computador", "notebook", "tablet", "smartphone", "iphone"]
}
```

If `categories.json` is present, it will be used automatically.

## Example

### Input CSV Format

```
date,title,amount
2025-05-01,Restaurant A,50.00
2025-05-02,Market B,30.00
2025-05-03,Health Service C,-20.00
2025-05-04,Store X Parcela 1/3,100.00
2025-06-04,Store X Parcela 2/3,100.00
2025-07-04,Store X Parcela 3/3,100.00
```

### Output CSV Format

```
date,title,amount,category
2025-05-01,Restaurant A,50.00,restaurants
2025-05-02,Market B,30.00,market
2025-05-04,Store X,300.00,others
```

### Output PDF

- First page: Pie chart and summary table of categories and their percentages.
- Second page: Transactions for each category, sorted from highest to lowest amount.

## Features

- **Automatic categorization** of transactions using customizable keywords.
- **Negative amounts** are filtered out automatically.
- **Installment merging** for transactions with "Parcela X/Y".
- **Custom categories** via `categories.json` (no code changes needed).
- **Multiple CSV support**.
- **CSV and PDF output**: Organized CSV and a detailed PDF report with summary, pie chart, and detailed tables.
- **All tables and charts are sorted** from highest to lowest amount for clarity.
- **Interactive GUI**: View, filter, and drill down into your spending.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.