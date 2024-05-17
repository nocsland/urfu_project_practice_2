import os

import torch
from tqdm import tqdm
from transformers import BigBirdTokenizer, BigBirdModel


# Функция для чтения текста из файлов с сохранением метаинформации
def read_text_from_files(file_paths):
    texts = []
    meta_info = []
    for file_path in file_paths:
        # Проверяем, является ли путь файлом
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            texts.append(text)
            # Сохраняем метаинформацию о файле
            file_info = {
                "file_name": os.path.basename(file_path),
                "file_path": file_path,
                # Другие поля метаинформации, если нужно
            }
            meta_info.append(file_info)
    return texts, meta_info


# Функция для разбиения текста на чанки с заданным размером
def split_text_into_chunks(texts, chunk_size):
    chunks = []
    for text in texts:
        words = text.split()
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
    return chunks


# Функция для создания эмбеддингов с использованием BigBird
def create_embeddings(chunks):
    # Загружаем предобученную модель и токенайзер BigBird
    tokenizer = BigBirdTokenizer.from_pretrained('google/bigbird-roberta-base')
    model = BigBirdModel.from_pretrained('google/bigbird-roberta-base')

    embeddings = []
    for chunk in tqdm(chunks, desc="Creating embeddings"):
        # Токенизация текста
        inputs = tokenizer(chunk, return_tensors='pt', truncation=True, padding=True, max_length=4096)
        with torch.no_grad():
            outputs = model(**inputs)
        # Получаем эмбеддинги
        chunk_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        embeddings.append(chunk_embedding)
    return embeddings


if __name__ == "__main__":
    # Папка с файлами текста
    text_folder = "../data/result_text"

    # Список путей к файлам текста (включая файлы из вложенных папок)
    file_paths = []
    for root, dirs, files in os.walk(text_folder):
        for file_name in files:
            file_paths.append(os.path.join(root, file_name))

    # Чтение текста из файлов с сохранением метаинформации
    texts, meta_info = read_text_from_files(file_paths)

    # Параметр для определения размера чанков (например, количество слов)
    chunk_size = 100  # Можно изменить на нужное значение

    # Разбиение текста на чанки с заданным размером
    chunks = split_text_into_chunks(texts, chunk_size)

    # Создание эмбеддингов для чанков текста
    chunk_embeddings = create_embeddings(chunks)

    # Вывод эмбеддингов чанков и метаинформации
    # for i, (chunk_embedding, file_info) in enumerate(zip(chunk_embeddings, meta_info)):
    #     print(f"Chunk {i + 1}: {chunk_embedding}")
    #     print("Meta Info:", file_info)
