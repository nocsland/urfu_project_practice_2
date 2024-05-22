import json
from collections import defaultdict
from search_engine import read_validation_questions


# Функция для загрузки JSON данных
def load_json_data(file_path):
    with open(file_path, encoding='utf-8') as file:
        data = json.load(file)
    return data


# Функция для сравнения валидационных вопросов с JSON данными
def compare_and_score(validation_data, json_data):
    scores = defaultdict(int)
    total_weight = len(validation_data)
    for question, material in validation_data.items():
        # print(question, material)
        # input()
        found = False
        for item in json_data:
            if item['question'] == question:
                # print(item['question'])
                # input()
                for result in item['results']:
                    # print(result)
                    # input()
                    if result[0].replace('_', ';') == material:
                        # print(result[0])
                        # print(item['results'].index(result))
                        # input()
                        weight = 1 / (item['results'].index(result) + 1)
                        scores[material] += weight
                        # print(weight)
                        found = True
                        break
                if found:
                    break
    return scores, total_weight


# Функция для вычисления процента правильных ответов
def calculate_percentage(scores, total_weight):
    total_score = sum(scores.values())
    # print(total_score, total_weight)
    percentage = (total_score / total_weight) * 100
    return percentage


# Главная функция
def main():
    validation_file = "data/Answer and Question.txt"
    json_file = "data/processed/search_results.json"

    validation_data = read_validation_questions(validation_file)
    json_data = load_json_data(json_file)

    scores, total_weight = compare_and_score(validation_data, json_data)
    percentage = calculate_percentage(scores, total_weight)

    print(f"Процент правильных ответов: {percentage:.2f}%")


if __name__ == "__main__":
    main()
