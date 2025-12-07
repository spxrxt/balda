import os


def load_dictionary(file_path="data/russian_words.txt", min_word_length=3):
    """
    Загружает словарь из текстового файла. Каждое слово в верхнем регистре.
    Возвращает множество слов для быстрого поиска.
    """
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл словаря '{file_path}' не найден.")
        print("Убедитесь, что словарь 'russian_words.txt' находится в папке 'data'.")
        return set()

    words = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().upper()  # Удаляем пробелы и переводим в верхний регистр
                if word.isalpha() and len(word) >= min_word_length:  # Проверяем, что это только буквы и нужной длины
                    words.add(word)
        print(f"Словарь загружен успешно. Всего слов: {len(words)}")
        return words
    except Exception as e:
        print(f"Ошибка при загрузке словаря: {e}")
        return set()


def is_word_valid(word, dictionary):
    """Проверяет, существует ли слово в словаре."""
    return word.upper() in dictionary


if __name__ == "__main__":
    print("--- Тестирование Dictionary Handler ---")

    # Создадим временный тестовый файл словаря
    test_dir = "data"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    test_file_path = os.path.join(test_dir, "test_dict.txt")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write("Пример\nслово\nТест\n123\nАа\nбал\n")

    test_dict = load_dictionary(test_file_path, min_word_length=2)  # Для теста возьмем мин. длину 2
    print(f"Загруженный тестовый словарь: {test_dict}")

    assert is_word_valid("Пример", test_dict) == True
    assert is_word_valid("СЛОВО", test_dict) == True
    assert is_word_valid("ТЕСТ", test_dict) == True
    assert is_word_valid("Бал", test_dict) == True
    assert is_word_valid("НЕСУЩЕСТВУЕТ", test_dict) == False
    assert is_word_valid("АА", test_dict) == True  # Длина 2

    # Удалим тестовый файл
    os.remove(test_file_path)
    os.rmdir(test_dir)

    print("Тестирование Dictionary Handler завершено.")