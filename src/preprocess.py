import chardet
import os
import pandas as pd
import spacy
import random
from bs4 import BeautifulSoup
from tqdm import tqdm

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
def read_html_files(directory, num_files=1000):
    files = [f for f in os.listdir(directory) if f.endswith('.html')]
    # Выбираем минимум из num_files файлов или меньше, если их меньше
    selected_files = random.sample(files, min(len(files), num_files))
    articles = []
    for filename in tqdm(selected_files,
                         desc=f"Read HTML files from {directory}:"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                # Извлечение части заголовка до тире
                title = title_tag.string.split(' - ')[0].strip()  # type: ignore # noqa: E501
                title = title.split(';')[0].strip().replace('"', '')
                title = title.replace('\xa0', ' ')
                title = title.replace('/', ' ')
                title = title.replace('_', ' ')
                title = title.replace('  ', ' ')
                title = title.replace('?', '')
                # надо бы сделать на основе регулярных выражений
            else:
                title = None
            text = soup.get_text(separator=' ')
            articles.append(
                {'filename': filename, 'title': title, 'text': text})
    return articles


# Функция для чтения URL-адресов из текстовых файлов
def read_urls(directory):
    url_dict = {}
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    for txt_file in txt_files:
        filepath = os.path.join(directory, txt_file)
        with open(filepath, 'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        # print(encoding)
        with open(filepath, 'r', encoding=encoding) as f:
            lines = f.readlines()
        for line in lines:
            title = line.strip().split(';')[0].replace('"', '')
            title = title.split(' - ')[0].strip()
            title = title.replace('\xa0', ' ')
            title = title.replace('/', ' ')
            title = title.replace('_', ' ')
            title = title.replace('  ', ' ')
            title = title.replace('?', '')
            url = line.strip().split(';')[-1]
            url_dict[title] = url
    return url_dict


# Объединение данных из HTML-файлов и URL-адресов
def get_data():
    all_articles = []
    # Получаем список всех поддиректорий
    subdirs = next(os.walk(data_dir))[1]
    for subdir in subdirs:
        directory = os.path.join(data_dir, subdir)
        articles = read_html_files(directory)
        all_articles.extend(articles)

    url_dict = read_urls(data_dir)

    for article in tqdm(all_articles, desc="Read URLs:"):
        title = article['title']
        if title in url_dict:
            article['url'] = url_dict[title]
        else:
            article['url'] = None
    return all_articles


# Функция очистки и нормализации текста с использованием SpaCy
def preprocess_text(text):
    doc = nlp(text)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space]
    cleaned_text = ' '.join(tokens).strip()
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
for article in tqdm(data, desc="Preprocess data:"):
    article['cleaned_text'] = preprocess_text(article['text'])
    # article['summary'] = create_summary(article['cleaned_text'])

# Преобразование данных в DataFrame
df = pd.DataFrame(data)

# Проверка существования директории и её создание при необходимости
os.makedirs('data/processed', exist_ok=True)

# Сохранение предобработанных данных
# df.to_csv('data/processed/cleaned_data.csv', index=False)
df.to_json(
    'data/processed/cleaned_data.json',
    orient='records',
    # lines=True,
    force_ascii=False,
    )
