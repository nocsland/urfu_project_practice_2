import os
from bs4 import BeautifulSoup
from tqdm import tqdm


def clean_text(text):
    # Заменяем все NBSP на обычные пробелы
    cleaned_text = text.replace('\xa0', ' ')
    return cleaned_text


def html_to_text(html_content):
    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Извлекаем текст из HTML
    paragraphs = soup.find_all('p')
    text = [p.get_text(strip=True) for p in paragraphs]

    # Очищаем текст от NBSP
    cleaned_text = [clean_text(p) for p in text]

    # Объединяем текст с разделителем между абзацами
    full_text = '\n'.join(cleaned_text)
    return full_text


def html_to_json(html_file, output_dir):
    # Открываем HTML-файл для чтения
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Преобразуем HTML в текст
    text = html_to_text(html_content)

    # Получаем путь к файлу относительно исходной директории
    relative_path = os.path.relpath(html_file, html_dir)
    # Формируем путь для сохранения текстового файла
    text_dir = os.path.join(output_dir, os.path.dirname(relative_path))
    # Создаем вложенные каталоги, если они не существуют
    os.makedirs(text_dir, exist_ok=True)

    # Получаем имя файла без расширения
    file_name = os.path.splitext(os.path.basename(html_file))[0]

    # Сохраняем текст в текстовом файле
    text_file = os.path.join(text_dir, f"{file_name}.txt")
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)

    # Убираем печать для улучшения производительности
    # print(f"Файл {text_file} успешно создан.")


def process_html_files(html_dir, output_dir):
    # Перебираем все файлы и подкаталоги в указанной директории
    html_files = []
    for root, dirs, files in os.walk(html_dir):
        for file_name in files:
            if file_name.endswith(".html"):
                html_file = os.path.join(root, file_name)
                html_files.append(html_file)

    # Используем tqdm для отображения прогресса
    for html_file in tqdm(html_files, desc="Processing HTML files"):
        html_to_json(html_file, output_dir)


# Папка с HTML-файлами
html_dir = "../data/source_text"

# Папка для сохранения текстовых файлов
output_dir = "../data/result_text"

# Обработка HTML-файлов во всех подкаталогах
process_html_files(html_dir, output_dir)
