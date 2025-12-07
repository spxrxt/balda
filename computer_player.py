import random
import os


class ComputerPlayer:
    def __init__(self, game_instance):
        self.game = game_instance
        self.min_word_length = 3  # Минимальная длина слова для поиска

    def make_computer_move(self):
        """
        Очень простой ИИ: ищет первое возможное место для буквы
        и пытается составить любое допустимое слово.
        """
        board = self.game.get_board()
        board_size = self.game.board_size
        dictionary = self.game.dictionary
        used_words = self.game.get_used_words()

        # Шаг 1: Найти все возможные пустые клетки, примыкающие к занятым
        possible_placements = []
        for r in range(board_size):
            for c in range(board_size):
                if self.game.is_cell_empty(r, c):
                    valid, _ = self.game.is_valid_placement(r, c, 'А')  # Просто проверка на примыкание
                    if valid:
                        possible_placements.append((r, c))

        random.shuffle(possible_placements)  # Перемешиваем, чтобы не всегда было одно и то же место

        # Шаг 2: Для каждой такой клетки и каждой буквы, попробовать составить слово
        alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

        for r_new, c_new in possible_placements:
            for new_letter in alphabet:
                # Временно помещаем букву для поиска слов
                original_value = board[r_new][c_new]
                board[r_new][c_new] = new_letter

                # Теперь ищем слова, используя эту новую букву
                # Этот шаг является самой сложной частью для ИИ.
                # Для примитивного ИИ мы будем просто перебирать
                # все возможные слова, которые могут быть сформированы
                # из 3-5 букв на поле, включая новую.

                # Упрощение: будем искать слова только по горизонтали/вертикали
                # и только в непосредственной близости от новой буквы.

                # Поиск по горизонтали
                for start_c in range(max(0, c_new - 4), min(board_size, c_new + 1)):  # Длина слова 3-5
                    current_word_chars = []
                    current_word_coords = []
                    for c_scan in range(start_c, min(board_size, start_c + 5)):
                        if board[r_new][c_scan] != ' ':
                            current_word_chars.append(board[r_new][c_scan])
                            current_word_coords.append((r_new, c_scan))

                            if len(current_word_chars) >= self.min_word_length:  # ИСПРАВЛЕНО: используем self.min_word_length
                                potential_word = "".join(current_word_chars)
                                # Используем is_word_valid из game_logic или проверяем в словаре
                                if (new_letter in potential_word) and (potential_word in dictionary) and (
                                        potential_word not in used_words):
                                    # Нашли потенциальное слово!
                                    # Проверим, что новая буква используется и что координаты верны

                                    # Восстанавливаем исходное значение клетки
                                    board[r_new][c_new] = original_value

                                    # Делаем "реальный" ход
                                    move_successful, move_msg = self.game.make_move(
                                        r_new, c_new, new_letter, current_word_coords)
                                    if move_successful:
                                        return True, new_letter, r_new, c_new, potential_word, len(potential_word)

                        else:  # Если встретили пробел, слово прерывается
                            current_word_chars = []
                            current_word_coords = []
                            if c_scan > c_new + 1:  # Если прошли мимо новой буквы, но слово не сформировалось
                                break

                # Поиск по вертикали (аналогично)
                for start_r in range(max(0, r_new - 4), min(board_size, r_new + 1)):
                    current_word_chars = []
                    current_word_coords = []
                    for r_scan in range(start_r, min(board_size, start_r + 5)):
                        if board[r_scan][c_new] != ' ':
                            current_word_chars.append(board[r_scan][c_new])
                            current_word_coords.append((r_scan, c_new))

                            if len(current_word_chars) >= self.min_word_length:  # ИСПРАВЛЕНО: используем self.min_word_length
                                potential_word = "".join(current_word_chars)
                                if (new_letter in potential_word) and (potential_word in dictionary) and (
                                        potential_word not in used_words):
                                    # Восстанавливаем исходное значение клетки
                                    board[r_new][c_new] = original_value

                                    move_successful, move_msg = self.game.make_move(
                                        r_new, c_new, new_letter, current_word_coords)
                                    if move_successful:
                                        return True, new_letter, r_new, c_new, potential_word, len(potential_word)
                        else:
                            current_word_chars = []
                            current_word_coords = []
                            if r_scan > r_new + 1:
                                break

                # Если слово не найдено, восстанавливаем исходное значение клетки
                board[r_new][c_new] = original_value

        return False, None, None, None, None, None  # Не удалось сделать ход


# Функция для проверки слова (если не импортируется из game_logic)
def is_word_valid(word, dictionary):
    """Проверяет, находится ли слово в словаре."""
    return word in dictionary


if __name__ == "__main__":
    print("--- Тестирование Computer Player (простейший ИИ) ---")

    # Создадим временный тестовый файл словаря
    test_dir = "data"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    test_file_path = os.path.join(test_dir, "russian_words.txt")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write("ПЛАЦ\nПЛОТ\nСТОЛ\nЛОЖЬ\nБАЛДА\nДАМБА\n")

    from game_logic import BaldaGame  # Импортируем BaldaGame для тестирования

    game = BaldaGame(board_size=5, initial_word="СТОЛ", dictionary_path=test_file_path)
    # Поле:
    #      С Т О Л
    # Должен найти "ЛОЖЬ" или "ПЛАЦ"

    print("\nНачальное поле:")
    for row in game.get_board():
        print(" ".join(row))

    comp_player = ComputerPlayer(game)

    print("\nПопытка хода компьютера:")

    # Чтобы ИИ мог найти слово, нужно создать условия
    # Допустим, мы хотим получить "ЛОЖЬ", используя буквы Л, О, Ж
    # Л находится в (2,3), О в (2,2)
    # ИИ должен поставить Ж в (3,2)
    # Тогда слово будет: (2,3) Л, (2,2) О, (3,2) Ж
    #
    # С(2,0) Т(2,1) О(2,2) Л(2,3)
    #
    #      Ж(3,2)

    # Это сложно для простого перебора.
    # Простейший ИИ может просто ставить буквы и проверять горизонталь/вертикаль

    # Давайте создадим более благоприятные условия для ИИ
    game_for_ai = BaldaGame(board_size=5, initial_word="ПЛАЦ", dictionary_path=test_file_path)
    game_for_ai.board[1][2] = 'Т'  # Добавим Т, чтобы можно было сделать ПЛОТ
    # Поле:
    #      П Л А Ц
    #        Т
    #
    # ИИ должен добавить О в (2,2) или (3,2) и составить ПЛОТ
    print("\nПоле для ИИ:")
    for row in game_for_ai.get_board():
        print(" ".join(row))

    ai_success, letter, r, c, word, score = ComputerPlayer(game_for_ai).make_computer_move()
    if ai_success:
        print(f"ИИ сделал ход: буква '{letter}' в ({r},{c}), составил слово '{word}' (очки: {score})")
        print("\nПоле после хода ИИ:")
        for row in game_for_ai.get_board():
            print(" ".join(row))
    else:
        print("ИИ не смог сделать ход.")

    # Удалим тестовый файл
    os.remove(test_file_path)
    os.rmdir(test_dir)
    print("Тестирование Computer Player завершено.")