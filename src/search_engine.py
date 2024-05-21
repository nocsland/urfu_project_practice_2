import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Загрузка предобработанных данных
data = pd.read_json('data/processed/cleaned_data.json', orient='records')


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
            self.data.iloc[i]['title'],
            # self.data.iloc[i]['summary'],
            self.data.iloc[i]['url']) for i in related_docs_indices]
        return results


# Инициализация парсера
data_parser = EnhancedParser(data)

questions = [
    "Как быть если заказчик требует водителя с мед книжкой?",
    "Что входит в доставку в гипермаркеты?",
    "Как занести контакт в черный список?",
    "Доступна ли перевозка грузов к Киргизию?",
    "Как найти груз по номеру интернет заказа?",
    "Как изменить страховую сумму при оформлении груза?",
    "Возможна ли доставка день в день? Какие интервалы доставки?",
    "Что делать, если клиент предоставил новый номер для оповещения?",
    "Почему не выходят на печать чеки об оплате и ПКО не отображается в реестре?",
    "Как клиент может изменить дату авизации в личном кабинете?",
    "Клиент спрашивает, для чего мы запрашиваем письма от клиента, при предоставление ему очередного спец условия",
    "Что написать клиенту, который просит полный доступ клеиному кабинету?",
    "Какая упаковк5а испольтзуется при перевозке автомобильных стекол?",
    "Сколько времени может проработать подметальная машина?",
    "Что делать, если клиент отказывается получения сопроводительных документов?",
    "Какие есть размеры палетных рам?",
    "Как осуществить Контроль выполнения НТМЦ?",
    "При отправке грузов в Минск прямые или транзитные рейсы?",
    "Какие документы нужны для выдачи грузов в Беларусь (для физ. и юр. лиц)?",
    "Что делать, если клиент выбрал способ подписания Договорных документов на бумаге?",
    ]

results = []
for question in questions:
    results.append({"question": question, "results": data_parser.search(question)})

# Сохранение результатов в файл JSON
with open('search_results.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)
