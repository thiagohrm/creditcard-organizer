import pandas as pd
import argparse
from categorizer import TransactionCategorizer
from utils import read_csv, write_csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(input_file, categorized_transactions):
    output_pdf = input_file.replace('.csv', '.pdf')
    summary = categorized_transactions.groupby('category')['amount'].sum().reset_index()
    total = summary['amount'].sum()
    summary['percentage'] = (summary['amount'] / total * 100).round(2)

    # Prepare summary data for table
    summary_data = [['Category', 'Sum of amount', 'Percentage']]
    for _, row in summary.iterrows():
        summary_data.append([
            row['category'],
            f"{row['amount']:.2f}",
            f"{int(round(row['percentage']))}%"
        ])
    summary_data.append(['Total', f"{total:.2f}", '100%'])

    # Create PDF
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Summary by Category", styles['Title']))
    t = Table(summary_data, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-2), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 1, colors.grey),
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightblue),
    ]))
    elements.append(t)
    elements.append(PageBreak())

    # Transactions by category
    elements.append(Paragraph("Transactions by Category", styles['Title']))
    for category in summary['category']:
        elements.append(Paragraph(f"<b>{category.capitalize()}</b>", styles['Heading2']))
        cat_df = categorized_transactions[categorized_transactions['category'] == category]
        trans_data = [['Date', 'Title', 'Amount']]
        for _, row in cat_df.iterrows():
            trans_data.append([row['date'], row['title'], f"{row['amount']:.2f}"])
        trans_table = Table(trans_data, hAlign='LEFT')
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (2,1), (2,-1), 'RIGHT'),
        ]))
        elements.append(trans_table)
        elements.append(Spacer(1, 12))
    doc.build(elements)

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
    generate_pdf(args.input_file, categorized_transactions)

if __name__ == '__main__':
    main()