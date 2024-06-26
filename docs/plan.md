# План 

1. **Подготовка данных**:
    - Преобразовать HTML документы в текстовый формат, удалив HTML-теги и другие форматирования.
    - Провести предварительную обработку текста, включая удаление стоп-слов, лемматизацию, токенизацию и т. д.
    - Создать базу данных или индекс для эффективного поиска информации. **(Реализовано)**

2. **Обучение ML модели**:
    - Выбрать подходящую модель для обучения, например, модель Question-Answering на основе BERT или другой
      предобученной нейросети.
    - Использовать обучающий набор данных, включающий вопросы и соответствующие ответы из документов.
    - Обучить модель на этих данных, настроив гиперпараметры и оценив ее производительность.

3. **Разработка телеграм-бота**:
    - Использовать Telegram API для создания бота.
    - Реализовать функционал бота для взаимодействия с пользователем, принимая вопросы и отображая ответы. **(Реализовано)**
    - Интегрировать ML модель в бота, чтобы он мог формулировать ответы на вопросы, используя обученную модель.

4. **Тестирование и оптимизация**:
    - Провести тестирование бота на различных вопросах, включая как общие, так и специфические.
    - Оптимизировать производительность бота и модели, например, путем кэширования результатов или использования
      асинхронных запросов.

5. **Мониторинг и обновление**:
    - Регулярно мониторить работу бота и собирать обратную связь от пользователей.
    - Проводить обновления модели при необходимости, чтобы улучшить качество ответов.