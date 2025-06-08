import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import io
import numpy as np
import re

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

        # --- Bar chart with trend line for this category ---
        if not cat_df.empty:
            # Group by date and sum
            date_group = cat_df.groupby('date')['amount'].sum().reset_index()
            # Sort by date
            date_group['date'] = pd.to_datetime(date_group['date'])
            date_group = date_group.sort_values('date')
            # Prepare data
            x = np.arange(len(date_group))
            y = date_group['amount'].values
            # Trend line
            if len(x) > 1:
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                trend = p(x)
            else:
                trend = y

            # Plot
            fig2, ax2 = plt.subplots(figsize=(5, 2.5))
            formatted_dates = date_group['date'].dt.strftime('%Y-%m-%d')
            ax2.bar(formatted_dates, y, color='skyblue', label='Amount')
            ax2.plot(formatted_dates, trend, color='red', linewidth=2, label='Trend')
            ax2.set_title(f"Spending Trend for {category.capitalize()}")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Amount")
            ax2.tick_params(axis='x', rotation=45)
            ax2.legend()
            plt.tight_layout()

            # Save to buffer
            bar_buffer = io.BytesIO()
            plt.savefig(bar_buffer, format='PNG')
            plt.close(fig2)
            bar_buffer.seek(0)
            elements.append(Image(bar_buffer, width=350, height=150))
            elements.append(Spacer(1, 8))

        # --- Transactions table ---
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

def merge_installments(df):
    """
    Merge transactions with 'Parcela X/Y' in the title, summing their amounts.
    Keeps other transactions unchanged.
    """
    # Extract base title (without 'Parcela X/Y')
    def base_title(title):
        match = re.match(r"(.+?)\s+Parcela\s+\d+/\d+", title, re.IGNORECASE)
        return match.group(1).strip() if match else title.strip()

    df = df.copy()
    df['base_title'] = df['title'].apply(base_title)
    df['is_parcela'] = df['title'].str.contains(r'Parcela \d+/\d+', case=False, regex=True)

    # Group by base_title if it's an installment, else keep as is
    parcela_df = df[df['is_parcela']]
    non_parcela_df = df[~df['is_parcela']]

    if not parcela_df.empty:
        # For installments, sum amounts and keep the earliest date
        merged = parcela_df.groupby('base_title').agg({
            'amount': 'sum',
            'date': 'min'
        }).reset_index()
        merged['title'] = merged['base_title']
        merged = merged[['date', 'title', 'amount']]
        # Combine with non-installment transactions
        result = pd.concat([non_parcela_df[['date', 'title', 'amount']], merged], ignore_index=True)
    else:
        result = df[['date', 'title', 'amount']]

    return result