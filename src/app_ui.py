import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from categorizer import TransactionCategorizer
from utils import read_csv, generate_pdf, write_csv
from tkinter import simpledialog
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CreditCardOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Credit Card Organizer")
        self.geometry("1000x700")
        self.categorized_transactions = None
        self.summary = None
        self.current_csv = None  # Track current CSV file path

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.upload_tab = ttk.Frame(self.notebook)
        self.summary_tab = ttk.Frame(self.notebook)
        self.details_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.upload_tab, text='Upload CSV')
        # Do NOT add summary and details tabs here

        self.create_upload_tab()
        self.create_summary_tab()
        self.create_details_tab()

    def create_upload_tab(self):
        label = ttk.Label(self.upload_tab, text="Upload your credit card CSV file:")
        label.pack(pady=20)
        upload_btn = ttk.Button(self.upload_tab, text="Select CSV", command=self.upload_csv)
        upload_btn.pack()
        # Clean Data button
        clean_btn = ttk.Button(self.upload_tab, text="Clean Data", command=self.clean_data)
        clean_btn.pack(pady=5)
        # Label to show current CSV file
        self.csv_label = ttk.Label(self.upload_tab, text="No CSV loaded.")
        self.csv_label.pack(pady=10)
        # Label to show processing status
        self.processing_label = ttk.Label(self.upload_tab, text="", foreground="blue")
        self.processing_label.pack(pady=5)

    def create_summary_tab(self):
        self.summary_canvas = None
        self.summary_table = None
        # Add Export button only once
        self.export_btn = ttk.Button(self.summary_tab, text="Export to PDF", command=self.export_pdf_dialog)
        self.export_btn.pack(pady=10)
        # Frame for dynamic content
        self.summary_content = ttk.Frame(self.summary_tab)
        self.summary_content.pack(fill='both', expand=True)

    def create_details_tab(self):
        self.details_notebook = ttk.Notebook(self.details_tab)
        self.details_notebook.pack(fill='both', expand=True)

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        self.csv_label.config(text=f"Current CSV: {os.path.basename(file_path)}")
        self.processing_label.config(text="Processing...", foreground="blue")
        self.update_idletasks()
        try:
            transactions = read_csv(file_path)
            categories_json_path = os.path.join(os.path.dirname(__file__), 'categories.json')
            if os.path.exists(categories_json_path):
                categorizer = TransactionCategorizer(categories_json_path)
            else:
                categorizer = TransactionCategorizer()
            self.categorized_transactions = categorizer.categorize_transactions(transactions)
            self.current_csv = file_path
            # Add summary and details tabs if not present
            if self.summary_tab not in self.notebook.tabs():
                self.notebook.add(self.summary_tab, text='Summary')
            if self.details_tab not in self.notebook.tabs():
                self.notebook.add(self.details_tab, text='Details')
            self.show_summary()
            self.show_details()
            self.notebook.select(self.summary_tab)
            self.processing_label.config(text="")  # Clear processing message
        except Exception as e:
            self.processing_label.config(text="")
            messagebox.showerror("Error", f"Failed to process file: {e}")

    def clean_data(self):
        # Remove data from memory
        self.categorized_transactions = None
        self.summary = None
        self.current_csv = None
        # Remove summary and details tabs if present
        for tab in [self.summary_tab, self.details_tab]:
            try:
                self.notebook.forget(tab)
            except tk.TclError:
                pass
        # Reset labels
        self.csv_label.config(text="No CSV loaded.")
        self.processing_label.config(text="")

    def show_summary(self):
        # Only clear dynamic content, not the export button
        for widget in self.summary_content.winfo_children():
            widget.destroy()
        if self.categorized_transactions is None:
            return

        summary = self.categorized_transactions.groupby('category')['amount'].sum().reset_index()
        summary = summary.sort_values(by='amount', ascending=False)
        total = summary['amount'].sum()
        summary['percentage'] = (summary['amount'] / total * 100).round(2)
        self.summary = summary

        # Pie chart
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
        canvas = FigureCanvasTkAgg(fig, master=self.summary_content)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
        plt.close(fig)

        # Table
        table_frame = ttk.Frame(self.summary_content)
        table_frame.pack(fill='x', padx=10, pady=10)
        cols = ['Category', 'Sum of amount', 'Percentage']
        tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=8)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')
        for _, row in summary.iterrows():
            tree.insert('', 'end', values=(row['category'], f"{row['amount']:.2f}", f"{row['percentage']}%"))
        tree.insert('', 'end', values=('Total', f"{total:.2f}", '100%'))
        tree.pack(fill='x')

    def show_details(self):
        for tab in self.details_notebook.tabs():
            self.details_notebook.forget(tab)
        if self.categorized_transactions is None or self.summary is None:
            return
        for category in self.summary['category']:
            frame = ttk.Frame(self.details_notebook)
            self.details_notebook.add(frame, text=category.capitalize())

            cat_df = self.categorized_transactions[self.categorized_transactions['category'] == category]
            cat_df = cat_df.sort_values(by='amount', ascending=False)

            # Bar chart with trend line
            if not cat_df.empty:
                date_group = cat_df.groupby('date')['amount'].sum().reset_index()
                date_group['date'] = pd.to_datetime(date_group['date'])
                date_group = date_group.sort_values('date')
                x = range(len(date_group))
                y = date_group['amount'].values
                if len(x) > 1:
                    import numpy as np
                    z = np.polyfit(x, y, 1)
                    p = np.poly1d(z)
                    trend = p(x)
                else:
                    trend = y

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
                canvas2 = FigureCanvasTkAgg(fig2, master=frame)
                canvas2.draw()
                canvas2.get_tk_widget().pack(pady=10)
                plt.close(fig2)

            # Table of transactions
            table_frame = ttk.Frame(frame)
            table_frame.pack(fill='both', expand=True, padx=10, pady=10)
            cols = ['Date', 'Title', 'Amount']
            tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=10)
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, anchor='center')
            for _, row in cat_df.iterrows():
                tree.insert('', 'end', values=(row['date'], row['title'], f"{row['amount']:.2f}"))
            tree.pack(fill='both', expand=True)

    def export_pdf_dialog(self):
        if self.categorized_transactions is None or self.summary is None:
            messagebox.showwarning("No Data", "Please upload and process a CSV first.")
            return

        categories = list(self.summary['category'])
        dialog = CategoryExportDialog(self, categories)
        self.wait_window(dialog)
        selected = dialog.result
        if not selected or (isinstance(selected, list) and not selected):
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        if selected == "all":
            generate_pdf(file_path, self.categorized_transactions)
            messagebox.showinfo("Exported", f"Exported all categories to {file_path}")
        else:
            # Filter only selected categories
            filtered = self.categorized_transactions[self.categorized_transactions['category'].isin(selected)]
            generate_pdf(file_path, filtered)
            messagebox.showinfo("Exported", f"Exported selected categories to {file_path}")

    def generate_single_category_pdf(self, output_pdf, category, cat_df):
        import matplotlib.pyplot as plt
        import io
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors

        doc = SimpleDocTemplate(output_pdf)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph(f"Summary for Category: {category.capitalize()}", styles['Title']))

        # Bar chart with trend line
        if not cat_df.empty:
            date_group = cat_df.groupby('date')['amount'].sum().reset_index()
            date_group['date'] = pd.to_datetime(date_group['date'])
            date_group = date_group.sort_values('date')
            x = range(len(date_group))
            y = date_group['amount'].values
            if len(x) > 1:
                import numpy as np
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                trend = p(x)
            else:
                trend = y

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
            bar_buffer = io.BytesIO()
            plt.savefig(bar_buffer, format='PNG')
            plt.close(fig2)
            bar_buffer.seek(0)
            elements.append(Image(bar_buffer, width=350, height=150))
            elements.append(Spacer(1, 8))

        # Table of transactions
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
        doc.build(elements)

class CategoryExportDialog(tk.Toplevel):
    def __init__(self, parent, categories):
        super().__init__(parent)
        self.title("Select Categories to Export")
        self.selected = []
        self.vars = {}
        self.categories = categories
        self.result = None

        self.all_var = tk.BooleanVar()
        all_cb = ttk.Checkbutton(self, text="All", variable=self.all_var, command=self.toggle_all)
        all_cb.pack(anchor='w', padx=10, pady=(10, 0))

        self.cat_frame = ttk.Frame(self)
        self.cat_frame.pack(fill='x', padx=10, pady=10)
        for cat in categories:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(self.cat_frame, text=cat, variable=var, command=self.toggle_cat)
            cb.pack(anchor='w')
            self.vars[cat] = (var, cb)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', pady=10)
        export_btn = ttk.Button(btn_frame, text="Export", command=self.on_export)
        export_btn.pack(side='left', padx=5)
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self.destroy)
        cancel_btn.pack(side='left', padx=5)

    def toggle_all(self):
        state = tk.DISABLED if self.all_var.get() else tk.NORMAL
        for var, cb in self.vars.values():
            cb.config(state=state)
            if self.all_var.get():
                var.set(False)

    def toggle_cat(self):
        # If any category is checked, uncheck "All"
        if any(var.get() for var, _ in self.vars.values()):
            self.all_var.set(False)
            for var, cb in self.vars.values():
                cb.config(state=tk.NORMAL)

    def on_export(self):
        if self.all_var.get():
            self.result = "all"
        else:
            self.result = [cat for cat, (var, _) in self.vars.items() if var.get()]
        self.destroy()

if __name__ == '__main__':
    app = CreditCardOrganizerApp()
    app.mainloop()