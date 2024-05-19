import pandas as pd
import numpy as np
import re
import nltk
from nltk.tokenize import word_tokenize
from pymystem3 import Mystem
from nltk.corpus import stopwords
from concurrent.futures import ProcessPoolExecutor
from gensim.models import Word2Vec
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity


# Загружаем данные в датафрейм
df = pd.read_('путь_до_хайла_данных') # либо тут применить чдение данных чанками по файлам в цикле


# Предобработка текста
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# lemmatizer
# кошками → кошка
# бежал → бежать
# боязненных → боязненный
lemmatizer = Mystem()

def text_preprocessing(text):
  if isinstance(text, str):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('russian'))
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word)[0] for word in tokens]
    processed_text = ' '.join(tokens)
    return processed_text
  else:
    return ""

# Определение количества текстов и параллельная предобработка
texts = df['ключ_по_данным'].to_numpy()
with ProcessPoolExecutor() as executor:
    preprocessed_texts = list(executor.map(text_preprocessing, texts))

# Создание и обучение модели Word2Vec
model = Word2Vec(sentences=preprocessed_texts, vector_size=50, window=5, min_count=1, sg=0)

# Оптимизированная функция для создания векторов текстов
def text_to_vector(text):
    vector = np.zeros(model.vector_size)
    word_count = 0
    for word in text.split():
        if word in model.wv:
            vector += model.wv[word]
            word_count += 1
    if word_count > 0:
        vector /= word_count
    return vector

# Создание векторов для текстов
text_vectors = [text_to_vector(text) for text in preprocessed_texts]

# Рассчет матрицы косинусной схожести
similarity_matrix = cosine_similarity(text_vectors, text_vectors)

# Выставляем порог сходства
similarity_threshold = 0.9

# Выбор наиболее информативных текстов
selected_indices = []
used_indices = set()

n = len(df)
for i in range(n):
    if i in used_indices:
        continue

    max_word_count = 0
    most_informative_index = i

    for j in range(i+1, n):
        if similarity_matrix[i][j] > similarity_threshold:
            word_count_j = len(preprocessed_texts[j].split())

            if word_count_j > max_word_count:
                max_word_count = word_count_j
                most_informative_index = j

            used_indices.add(j)

    selected_indices.append(most_informative_index)

# Создание DataFrame с выбранными текстами
selected_df = df.iloc[selected_indices].copy()

# Тут скорее всего ошибаюсь, про кластеризацию, чтобы потом сделать маппинг на ссылку, но иначе пока не понимаю
# Как вариант кластеризация DBSCAN
eps = 0.2
min_samples = 1

# Предполагая, что selected_indices содержит индексы 800 выбранных текстов
selected_texts = [preprocessed_texts[i] for i in selected_indices]
selected_vectors = [text_to_vector(text) for text in selected_texts]

# Применяем DBSCAN к выбранным векторам
dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
cluster_labels = dbscan.fit_predict(selected_vectors)

# Назначяем метки кластеров selected_df
selected_df['cluster_label'] = cluster_labels

# Сохраняем результат и тут я не знаю что дальше делать ((
# Как привязать ссылки к меткам корректно ???
selected_df.to_excel('selected_texts.xlsx', index=False)
