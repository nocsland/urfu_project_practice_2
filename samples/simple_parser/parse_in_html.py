import os
from bs4 import BeautifulSoup


def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup


def find_text_in_html(html_soup, search_text):
    found_elements = html_soup.find_all(text=lambda text: search_text in str(text))
    return found_elements


def search_in_directory(directory_path, search_text):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith('.html'):
                file_path = os.path.join(root, file_name)
                parsed_html = parse_html_file(file_path)
                found_elements = find_text_in_html(parsed_html, search_text)
                if found_elements:
                    print(f"Найденные элементы в файле '{file_path}':")
                    for element in found_elements:
                        print(element)
                # else:
                #     print(f"Текст не найден в файле '{file_path}'.")


if __name__ == "__main__":
    directory_path = '../../data/source_text'  # Путь к каталогу с HTML файлами
    search_text = input("Введите запрос ")  # Текст, который вы ищете

    search_in_directory(directory_path, search_text)
