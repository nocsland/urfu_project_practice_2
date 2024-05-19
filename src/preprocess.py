import chardet
import os
import pandas as pd
import spacy
import random
from bs4 import BeautifulSoup

# Установка фиксированного значения seed для воспроизводимости результатов
random.seed(42)

# Загрузка русской модели SpaCy
# _sm - базовая модель для русского языка,
# включающая базовую лемматизацию и POS-теггинг
# _md - содержит более детализированные компоненты и данные
# для более точных предсказаний по сравнению с базовой
# _lg - содержит еще более детализированные и объемные компоненты
# для наилучшей точности предсказаний
nlp = spacy.load('ru_core_news_sm')

# Путь к папке с данными
data_dir = './data/source_text/'


# Функция для чтения данных из HTML-файлов
def read_html_files(directory, num_files=10):
    files = [f for f in os.listdir(directory) if f.endswith('.html')]
    random.shuffle(files)
    selected_files = files[:num_files]
    articles = []
    for filename in selected_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text(separator=' ')
            articles.append({'filename': filename, 'text': text})
    return articles


# Функция для чтения URL-адресов из текстовых файлов
def read_urls(file):
    url_dict = {}
    with open(file, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    # print(encoding)
    with open(file, 'r', encoding=encoding) as f:
        lines = f.readlines()
    for line in lines:
        title = line.strip().split(';')[0]
        url = line.strip().split(';')[1]
        filename = title + '.html'
        url_dict[filename] = {'title': title, 'url': url}
    return url_dict


# Объединение данных из HTML-файлов и URL-адресов
def get_data():
    all_articles = []
    categories = ['CMK', 'DRK', 'FTL', 'FT', 'OTP']
    for category in categories:
        directory = os.path.join(data_dir, category)
        articles = read_html_files(directory)
        url_file = os.path.join(data_dir, f"{category}.txt")
        url_dict = read_urls(url_file)

        for article in articles:
            filename = article['filename']
            if filename in url_dict:
                article.update(url_dict[filename])
            else:
                article['title'] = None
                article['url'] = None
            article['category'] = category
        all_articles.extend(articles)
    return all_articles


# Функция очистки и нормализации текста с использованием SpaCy
def preprocess_text(text):
    doc = nlp(text)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space]
    cleaned_text = ' '.join(tokens)
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text


# Функция для создания краткой выдержки из текста
'''
def create_summary(text, num_sentences=1):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    summary = ' '.join(sentences[:num_sentences])
    return summary
'''

# Чтение данных и их предобработка
data = get_data()
for article in data:
    article['cleaned_text'] = preprocess_text(article['text'])
    # article['summary'] = create_summary(article['cleaned_text'])

# Преобразование данных в DataFrame
df = pd.DataFrame(data)

# Проверка существования директории и её создание при необходимости
os.makedirs('data/processed', exist_ok=True)

# Сохранение предобработанных данных
df.to_csv('data/processed/cleaned_data.csv', index=False)
