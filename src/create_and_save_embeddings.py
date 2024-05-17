import os
import torch
import numpy as np
from tqdm import tqdm
from transformers import BigBirdTokenizer, BigBirdModel


def read_text_from_files(file_paths):
    texts = []
    meta_info = []
    for file_path in file_paths:
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            texts.append(text)
            file_info = {
                "file_name": os.path.basename(file_path),
                "file_path": file_path,
            }
            meta_info.append(file_info)
    return texts, meta_info


def split_text_into_chunks(texts, chunk_size):
    chunks = []
    for text in texts:
        words = text.split()
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
    return chunks


def create_embeddings(chunks, save_path):
    if os.path.exists(save_path):
        # Если файл с эмбеддингами уже существует, загружаем эмбеддинги из файла
        with open(save_path, 'rb') as f:
            chunk_embeddings = np.load(f)
    else:
        tokenizer = BigBirdTokenizer.from_pretrained('google/bigbird-roberta-base')
        model = BigBirdModel.from_pretrained('google/bigbird-roberta-base')

        chunk_embeddings = []
        for chunk in tqdm(chunks, desc="Creating embeddings"):
            inputs = tokenizer(chunk, return_tensors='pt', truncation=True, padding=True, max_length=4096)
            with torch.no_grad():
                outputs = model(**inputs)
            chunk_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            chunk_embeddings.append(chunk_embedding)

        # Сохраняем эмбеддинги в файл
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Создаем каталог, если его нет
        with open(save_path, 'wb') as f:
            np.save(f, np.array(chunk_embeddings))

    return chunk_embeddings


if __name__ == "__main__":
    text_folder = "../data/result_text"
    file_paths = [os.path.join(root, file_name) for root, _, files in os.walk(text_folder) for file_name in files]

    texts, meta_info = read_text_from_files(file_paths)
    chunk_size = 100

    save_path = "../data/embeddings/chunk_embeddings.npy"  # Путь для сохранения эмбеддингов
    chunks = split_text_into_chunks(texts, chunk_size)
    chunk_embeddings = create_embeddings(chunks, save_path)

    # Вывод эмбеддингов чанков и метаинформации
    # for i, (chunk_embedding, file_info) in enumerate(zip(chunk_embeddings, meta_info)):
    #     print(f"Chunk {i + 1}: {chunk_embedding}")
    #     print("Meta Info:", file_info)
