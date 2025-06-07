import pandas as pd

class TransactionCategorizer:
    def __init__(self):
        self.category_keywords = {
            'market': ['benedete', 'imperio', 'market', 'delta', 'assai', 'lojao', 'americanas'],
            'health': ['drogal', 'remedio', 'saude', 'raia', 'drogasil', 'pague menos'],
            'online services': ['netflix', 'youtube premium', 'google one', 'ifood', 'microsoft', 'office', 'apple', 'melimais'],
            'restaurants': ['restaurante', 'burger', 'mcdonalds', 'kissburgers', 'lanchonete', 'esfirraria', 'churros'],
            'automotive': ['posto', 'nutag', 'abastece', 'abasteceai', 'estacionamento', 'f park'],
            'taxes': ['pagamento recebido', 'txentregvisto'],
        }

    def categorize_title(self, title):
        title_lower = title.lower()
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    return category
        return 'others'

    def categorize_transactions(self, df):
        # Remove negative amounts
        df = df[df['amount'] >= 0].copy()
        # Categorize
        df['category'] = df['title'].apply(self.categorize_title)
        return df