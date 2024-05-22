import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Загрузка предобработанных данных
data = pd.read_json('data/processed/cleaned_data_sm.json', orient='records')


class EnhancedParser:
    def __init__(self, data):
        self.data = data
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(data['cleaned_text'])

    def search(self, query):
        query_vec = self.vectorizer.transform([query])
        cosine_similarities = cosine_similarity(
            self.tfidf_matrix, query_vec).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-7:-1]
        results = [(
            self.data.iloc[i]['filename'],
            # self.data.iloc[i]['summary'],
            self.data.iloc[i]['url']) for i in related_docs_indices]
        return results


# Функция для чтения валидационных вопросов из файла
def read_validation_questions(file_path):
    validation_data = dict()
    with open(file_path, encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith("Вопрос"):
                question = lines[i+1].strip()
            if lines[i].startswith("Материалы"):
                material = lines[i+1].strip()
                validation_data[question] = material
            i += 1
    return validation_data


# Инициализация парсера
data_parser = EnhancedParser(data)

validation_file = "data/Answer and Question.txt"

validation_data = read_validation_questions(validation_file)

questions = list(validation_data.keys())

results = []
for question in questions:
    results.append(
        {"question": question, "results": data_parser.search(question)})

# Сохранение результатов в файл JSON
with open('data/processed/search_results.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)
