import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import io

def read_csv(file_path):
    return pd.read_csv(file_path)

def write_csv(dataframe, file_path):
    dataframe.to_csv(file_path, index=False)

def filter_negative_transactions(transactions):
    return transactions[transactions['amount'] >= 0]

def generate_pdf(input_file, categorized_transactions):
    output_pdf = input_file.replace('.csv', '.pdf')
    # Sort summary by amount descending
    summary = categorized_transactions.groupby('category')['amount'].sum().reset_index()
    summary = summary.sort_values(by='amount', ascending=False)
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

    # Create pie chart using matplotlib
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        summary['amount'],
        labels=summary['category'],
        autopct='%1.0f%%',
        startangle=90,
        colors=plt.cm.Paired.colors
    )
    ax.set_title('Spending by Category')
    plt.tight_layout()

    # Save pie chart to a BytesIO buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='PNG')
    plt.close(fig)
    img_buffer.seek(0)

    # Create PDF
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Summary by Category", styles['Title']))

    # Add pie chart image
    img = Image(img_buffer, width=200, height=200)
    elements.append(img)
    elements.append(Spacer(1, 12))

    # Add summary table
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

    # Transactions by category (sorted by amount)
    elements.append(Paragraph("Transactions by Category", styles['Title']))
    for category in summary['category']:
        elements.append(Paragraph(f"<b>{category.capitalize()}</b>", styles['Heading2']))
        cat_df = categorized_transactions[categorized_transactions['category'] == category]
        # Sort transactions in this category by amount descending
        cat_df = cat_df.sort_values(by='amount', ascending=False)
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