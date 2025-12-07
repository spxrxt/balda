import os
from dictionary_handler import load_dictionary, is_word_valid


class BaldaGame:
    def __init__(self, board_size=5, initial_word="БАЛДА", dictionary_path="data/russian_words.txt"):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.used_words = set()
        self.players = {1: {'score': 0, 'name': 'Игрок 1'},
                        2: {'score': 0, 'name': 'Игрок 2'}}
        self.current_player_id = 1
        self.dictionary = load_dictionary(dictionary_path)

        # Инициализация поля начальным словом
        self._place_initial_word(initial_word.upper())

    def _place_initial_word(self, word):
        """Размещает начальное слово в центре поля."""
        if len(word) > self.board_size:
            print("Начальное слово слишком длинное для поля!")
            return

        start_col = (self.board_size - len(word)) // 2
        row = self.board_size // 2
        for i, char in enumerate(word):
            self.board[row][start_col + i] = char
        self.initial_word_coords = [(row, start_col + i) for i in range(len(word))]

    def get_current_player_name(self):
        return self.players[self.current_player_id]['name']

    def switch_player(self):
        """Переключает текущего игрока."""
        self.current_player_id = 1 if self.current_player_id == 2 else 2

    def get_board(self):
        """Возвращает текущее состояние игрового поля."""
        return self.board

    def is_cell_empty(self, row, col):
        """Проверяет, пуста ли ячейка."""
        return 0 <= row < self.board_size and \
            0 <= col < self.board_size and \
            self.board[row][col] == ' '

    def is_valid_placement(self, row, col, letter):
        """
        Проверяет, является ли размещение буквы валидным.
        1. В пределах поля.
        2. Ячейка пуста.
        3. Соседняя ячейка занята (есть связь с другими буквами).
        """
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False, "Координаты вне поля."
        if self.board[row][col] != ' ':
            return False, "Ячейка уже занята."
        if not letter.isalpha() or len(letter) != 1:
            return False, "Нужна одна буква."

        # Проверяем, есть ли хотя бы один сосед
        has_neighbor = False
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Верх, низ, лево, право
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and \
                    0 <= nc < self.board_size and \
                    self.board[nr][nc] != ' ':
                has_neighbor = True
                break

        if not has_neighbor:
            return False, "Новая буква должна примыкать к существующим."

        return True, ""

    def make_move(self, row, col, letter, word_coords):
        """
        Пытается совершить ход игрока.
        row, col: координаты новой/измененной буквы
        letter: новая буква
        word_coords: список кортежей (r, c) - координаты букв, составляющих слово
        """
        letter = letter.upper()

        # 1. Проверка правильности расположения новой буквы
        valid_placement, msg = self.is_valid_placement(row, col, letter)
        if not valid_placement:
            return False, msg

        # 2. Временное размещение буквы для проверки слова
        original_cell_char = self.board[row][col]
        self.board[row][col] = letter

        # 3. Проверка составленного слова
        composed_word, word_is_contiguous = self._get_composed_word(word_coords)

        self.board[row][col] = original_cell_char  # Возвращаем на место для следующего шага

        if not word_is_contiguous:
            return False, "Составленное слово должно быть непрерывным на поле."

        if not composed_word:
            return False, "Не удалось составить слово по указанным координатам."

        if not is_word_valid(composed_word, self.dictionary):
            return False, f"Слово '{composed_word}' не найдено в словаре или слишком короткое."

        if composed_word in self.used_words:
            return False, f"Слово '{composed_word}' уже использовано."

        # 4. Проверка, что новая буква используется в слове
        if (row, col) not in word_coords:
            return False, "Новая буква должна быть частью составленного слова."

        # 5. Все проверки пройдены, совершаем ход
        self.board[row][col] = letter  # Окончательно размещаем букву
        self.used_words.add(composed_word)
        self.players[self.current_player_id]['score'] += len(composed_word)

        return True, f"Отлично! Слово '{composed_word}' (очки: {len(composed_word)}) добавлено."

    def _get_composed_word(self, word_coords):
        """
        Собирает слово по заданным координатам и проверяет его непрерывность.
        Возвращает (слово, True/False - непрерывно ли слово)
        """
        if not word_coords:
            return "", False

        # Отсортируем координаты для уникального представления, но для проверки непрерывности
        # важен порядок обхода. Здесь предполагается, что пользователь вводит координаты в порядке.
        # Для более строгой проверки можно использовать BFS/DFS

        # Простейшая проверка на непрерывность: все буквы должны быть на поле и не быть пустыми
        for r, c in word_coords:
            if not (0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] != ' '):
                return "", False

        # Проверим, что все буквы слова фактически примыкают друг к другу на поле
        # (т.е. нет разрывов). Это упрощенная проверка, которая может быть улучшена.
        # Для Balda это обычно означает, что все буквы должны быть соседними в какой-то последовательности.
        # Для простоты пока просто соберем слово. Более сложная проверка потребует алгоритма обхода графа.

        # Для Балды: слово должно формироваться по соседним клеткам.
        # Упрощаем: просто собираем буквы. Валидация, что это именно "слово",
        # будет сделана по наличию в словаре.

        # Чтобы проверить непрерывность:
        # 1. Построим граф из указанных координат, где узлы - это буквы, а ребра - смежность.
        # 2. Проверим, что это связный граф.
        # 3. Проверим, что каждая буква в списке word_coords используется только один раз.

        # Более простой подход для Балды: пользователь вводит координаты
        # (r1,c1), (r2,c2), (r3,c3)...
        # Предполагаем, что он вводит их последовательно для слова.
        # Проверяем, что (r_i, c_i) и (r_{i+1}, c_{i+1}) являются соседними.

        collected_word_chars = []
        visited_coords = set()

        if len(word_coords) > 1:
            for i in range(len(word_coords) - 1):
                r1, c1 = word_coords[i]
                r2, c2 = word_coords[i + 1]

                # Проверка на уникальность координат внутри слова
                if (r1, c1) in visited_coords:
                    return "", False  # Повторное использование буквы в слове
                visited_coords.add((r1, c1))

                # Проверка на смежность
                if not ((abs(r1 - r2) == 1 and c1 == c2) or (abs(c1 - c2) == 1 and r1 == r2)):
                    return "", False  # Буквы не соседние

            # Добавим последнюю координату
            r_last, c_last = word_coords[-1]
            if (r_last, c_last) in visited_coords:
                return "", False  # Повторное использование буквы
            visited_coords.add((r_last, c_last))
        else:  # Слово из одной буквы (для Балды обычно не допускается, но для теста)
            if (word_coords[0][0], word_coords[0][1]) in visited_coords:
                return "", False
            visited_coords.add((word_coords[0][0], word_coords[0][1]))

        # Теперь собираем слово, предполагая, что оно непрерывно
        word = ""
        for r, c in word_coords:
            word += self.board[r][c]

        return word, True  # Здесь True, так как проверили смежность и уникальность

    def get_score(self, player_id):
        return self.players[player_id]['score']

    def get_used_words(self):
        return self.used_words


# Для тестирования модуля
if __name__ == "__main__":
    print("--- Тестирование Game Logic ---")

    # Создадим временный тестовый файл словаря для этого модуля
    test_dir = "data"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    test_file_path = os.path.join(test_dir, "russian_words.txt")  # Используем имя, которое игра ожидает
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write("БАЛДА\nСТОЛ\nЛОЖЬ\nДАМБА\n")  # Добавим слова для теста

    game = BaldaGame(board_size=5, initial_word="СТОЛ", dictionary_path=test_file_path)

    # Тестирование инициализации
    print("\nНачальное поле:")
    for row in game.get_board():
        print(" ".join(row))

    # Тестирование is_valid_placement
    print("\nТестирование is_valid_placement:")
    valid, msg = game.is_valid_placement(2, 2, 'О')
    print(f"Поле {2},{2} (О): {valid}, {msg}")  # Должно быть False (занято СТОЛ)
    valid, msg = game.is_valid_placement(1, 2, 'П')
    print(f"Поле {1},{2} (П): {valid}, {msg}")  # Должно быть True (примыкает к Т)

    # Тестирование make_move
    print("\nТестирование make_move:")
    # Попробуем сделать ход: добавить 'Ж' рядом с 'О' в СТОЛ, чтобы получить ЛОЖЬ
    # СТОЛ
    # 01234
    #  Т
    #  О
    #  Л
    # Поле:
    #      С Т О Л
    # 0:
    # 1:
    # 2:   С Т О Л
    # 3:
    # 4:

    # Пусть СТОЛ находится в (2,1), (2,2), (2,3), (2,4)
    # Если начальное слово "СТОЛ", то оно займет (2,0), (2,1), (2,2), (2,3)
    # Попробуем разместить Ж в (3,2) и составить ЛОЖЬ

    # Изначально: [' ', ' ', ' ', ' ', ' ']
    #            [' ', ' ', ' ', ' ', ' ']
    #            ['С', 'Т', 'О', 'Л', ' ']
    #            [' ', ' ', ' ', ' ', ' ']
    #            [' ', ' ', ' ', ' ', ' ']

    # Добавляем Ж в (3, 2), формируем слово ЛОЖЬ (из (2,3) Л, (2,2) О, (3,2) Ж, (2,1) Т - нет, не так)
    # L(2,3) O(2,2) J(3,2) S(2,1) -- нет, слово должно быть непрерывным на поле
    # Попробуем проще: БАЛДА. Пусть оно в (2,0), (2,1), (2,2), (2,3), (2,4)
    #                   Б А Л Д А
    # Добавим М в (3,3) и получим ДАМБА
    game_balda = BaldaGame(board_size=5, initial_word="БАЛДА", dictionary_path=test_file_path)

    # Изначальное поле:
    # Б А Л Д А
    #
    #
    #
    #

    # Попробуем создать слово "ДАМБА"
    # D(2,3) A(2,4) M(3,4) B(2,0) A(2,1) - это не непрерывно
    # Нужно: D(2,3) A(2,4) M(3,4) B(3,3) A(2,2)
    # Это сложно для первой итерации. Упростим:
    # Просто добавляем 'М' в (3, 2) и пытаемся составить "ДАМБА"
    # Это потребует, чтобы БАЛДА была B(2,0) A(2,1) L(2,2) D(2,3) A(2,4)
    # Мы хотим слово ДАМБА: D(2,3), A(2,4), M(3,4), B(3,3), A(2,2)
    # Буква М должна быть в (3,3)

    # Координаты для слова "ДАМБА"
    # D(2,3), A(2,4), M(3,4), B(3,3), A(2,2) - это 5 букв.
    # Добавляем 'М' в (3,3)
    move_successful, move_msg = game_balda.make_move(
        row=3, col=3, letter='М',
        word_coords=[(2, 3), (2, 4), (3, 4), (3, 3), (2, 2)]
        # Это неправильный порядок, нужно: (2,3) Д, (2,2) А, (3,2) М, (2,1) Б, (2,0) А - что-то сложно
    )
    # Для теста сделаем проще:
    # БАЛДА
    # Добавим Ж в (3,2) и попробуем составить ЛОЖЬ, используя Л(2,2), О(2,1) и Ж(3,2)
    # Предположим, что ЛОЖЬ (2,2) (2,1) (3,2) - это слово
    game_balda_test = BaldaGame(board_size=5, initial_word="БАЛДА", dictionary_path=test_file_path)
    move_successful, move_msg = game_balda_test.make_move(
        row=3, col=2, letter='Ж',
        word_coords=[(2, 2), (2, 1), (3, 2)]  # (Л, А, Ж) - это не ЛОЖЬ
    )
    print(f"Ход (ЛОЖЬ): {move_successful}, {move_msg}")  # Должно быть False

    # Скорректируем:
    # Инициализируем слово "СТОЛ", чтобы было слово "ЛОЖЬ"
    game_2 = BaldaGame(board_size=5, initial_word="СТОЛ", dictionary_path=test_file_path)
    # Поле:
    #       С Т О Л
    # Добавим Ж в (3,2)
    move_successful, move_msg = game_2.make_move(
        row=3, col=2, letter='Ж',
        word_coords=[(2, 3), (2, 2), (3, 2)]  # Л О Ж
    )
    print(f"Ход (ЛОЖЬ): {move_successful}, {move_msg}")

    if move_successful:
        print("\nПоле после хода:")
        for row in game_2.get_board():
            print(" ".join(row))
        print(f"Очки Игрока 1: {game_2.get_score(1)}")
        print(f"Использованные слова: {game_2.get_used_words()}")

    # Удалим тестовый файл
    os.remove(test_file_path)
    os.rmdir(test_dir)

    print("Тестирование Game Logic завершено.")