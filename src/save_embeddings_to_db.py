import faiss
import numpy as np


# Функция для загрузки эмбеддингов из файла
def load_embeddings(file_path):
    return np.load(file_path)


# Функция для сохранения эмбеддингов в Faiss
def save_embeddings_to_faiss(embeddings, faiss_index_path):
    # Создаем индекс для векторов
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Добавляем эмбеддинги в индекс
    index.add(embeddings)

    # Сохраняем индекс на диск
    faiss.write_index(index, faiss_index_path)
    print(f"Индекс сохранен в {faiss_index_path}")


# Функция для загрузки индекса Faiss и выполнения поиска
def search_faiss_index(faiss_index_path, query_vector, k=5):
    # Загружаем индекс
    index = faiss.read_index(faiss_index_path)

    # Выполняем поиск
    distances, indices = index.search(query_vector, k)
    return distances, indices


if __name__ == "__main__":
    # Загрузка эмбеддингов
    embeddings = load_embeddings("../data/embeddings/chunk_embeddings.npy")

    # Путь для сохранения индекса Faiss
    faiss_index_path = "../data/db_index/faiss_index.bin"

    # Сохранение эмбеддингов в Faiss
    save_embeddings_to_faiss(embeddings, faiss_index_path)

    # Пример выполнения поиска
    # Вектор запроса (должен быть того же размера, что и эмбеддинги)
    query_vector = embeddings[0:1]  # Для примера берем первый эмбеддинг

    # Выполнение поиска
    distances, indices = search_faiss_index(faiss_index_path, query_vector, k=3)

    # Вывод результатов поиска
    print("Результаты поиска:")
    for distance, index in zip(distances[0], indices[0]):
        print(f"Индекс: {index}, Расстояние: {distance}")
