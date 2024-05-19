import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Загрузка предобработанных данных
data = pd.read_csv('data/processed/cleaned_data.csv')


class EnhancedParser:
    def __init__(self, data):
        self.data = data
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(data['cleaned_text'])

    def search(self, query):
        query_vec = self.vectorizer.transform([query])
        cosine_similarities = cosine_similarity(
            self.tfidf_matrix, query_vec).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-4:-1]
        results = [(
            self.data.iloc[i]['category'],
            self.data.iloc[i]['title'],
            # self.data.iloc[i]['summary'],
            self.data.iloc[i]['url']) for i in related_docs_indices]
        return results


# Инициализация парсера
data_parser = EnhancedParser(data)

query = "как оформить груз из интернет магазина"
results = data_parser.search(query)
for result in results:
    category, title, url = result
    print(f"Категория: {category}\nЗаголовок: {title}\nСсылка: {url}\n")
