def clear_screen():
    """Очищает экран терминала (работает на большинстве систем)."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def display_welcome_message():
    """Выводит приветственное сообщение."""
    clear_screen()
    print("---------------------------------")
    print("        Добро пожаловать в игру 'БАЛДА'!")
    print("---------------------------------")
    print("Правила:")
    print("1. Введите координаты (строка, столбец) и букву для новой клетки.")
    print("2. Затем введите координаты букв (строка, столбец), составляющих новое слово,")
    print("   включая только что добавленную букву. Каждая буква должна быть использована один раз.")
    print("3. Новое слово должно быть не короче 3 букв и существовать в словаре.")
    print("4. Буквы слова должны быть непрерывны на поле.")
    print("---------------------------------")


def get_game_mode():
    """Запрашивает у пользователя выбор режима игры."""
    while True:
        print("\nВыберите режим игры:")
        print("1. Против друга")
        print("2. Против компьютера")
        choice = input("Ваш выбор (1 или 2): ")
        if choice == '1':
            return "player_vs_player"
        elif choice == '2':
            return "player_vs_computer"
        else:
            print("Некорректный выбор. Пожалуйста, введите 1 или 2.")


def display_board(board):
    """Отображает игровое поле в консоли."""
    board_size = len(board)
    print("\n   " + " ".join([str(i) for i in range(board_size)]))  # Номера столбцов
    print("  " + "---" * board_size)
    for r_idx, row in enumerate(board):
        display_row = []
        for char in row:
            display_row.append(char if char != ' ' else '_')  # Заменяем пробелы на '_' для лучшей видимости
        print(f"{r_idx} | " + " ".join(display_row) + " |")
    print("  " + "---" * board_size)


def get_player_move_input(player_name, board_size):
    """
    Получает от игрока ввод для хода:
    координаты новой буквы, саму букву и координаты составленного слова.
    """
    print(f"\nХод игрока {player_name}:")

    # 1. Новая буква
    while True:
        try:
            row_str, col_str = input("Введите координаты новой буквы (строка столбец, например '2 3'): ").split()
            row, col = int(row_str), int(col_str)
            letter = input("Введите новую букву: ").upper()
            if not (0 <= row < board_size and 0 <= col < board_size) or len(letter) != 1 or not letter.isalpha():
                print("Некорректный ввод. Убедитесь, что координаты в пределах поля, а буква одна и является алфавитной.")
                continue
            break
        except ValueError:
            print("Некорректный формат. Введите два числа, затем одну букву.")
        except IndexError:
            print("Некорректный формат. Введите два числа через пробел.")

    # 2. Координаты слова
    word_coords_list = []
    print("Теперь введите координаты букв, составляющих слово (по одной паре 'строка столбец' за раз).")
    print("Когда закончите, введите 'готово'.")

    while True:
        coord_input = input(f"Координаты {len(word_coords_list) + 1}-й буквы (строка столбец / 'готово'): ").lower()
        if coord_input == 'готово':
            break

        try:
            r_str, c_str = coord_input.split()
            r, c = int(r_str), int(c_str)
            if not (0 <= r < board_size and 0 <= c < board_size):
                print("Координаты вне поля. Попробуйте еще раз.")
                continue
            word_coords_list.append((r, c))
        except ValueError:
            print("Некорректный формат. Введите два числа через пробел или 'готово'.")
        except IndexError:
            print("Некорректный формат. Введите два числа через пробел или 'готово'.")

    return row, col, letter, word_coords_list


def display_message(message):
    """Выводит общее сообщение."""
    print(message)


def display_scores(scores):
    """Отображает текущие очки игроков."""
    print("\n--- Текущие очки ---")
    for player_id, data in scores.items():
        print(f"{data['name']}: {data['score']} очков")
    print("--------------------")


def ask_to_play_again():
    """Спрашивает игрока, хочет ли он сыграть снова."""
    while True:
        choice = input("Хотите сыграть снова? (да/нет): ").lower()
        if choice in ['да', 'yes', 'д', 'y']:
            return True
        elif choice in ['нет', 'no', 'н', 'n']:
            return False
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")


if __name__ == "__main__":
    print("--- Тестирование User Interface ---")

    display_welcome_message()

    mode = get_game_mode()
    print(f"Выбран режим: {mode}")

    test_board = [
        ['Б', ' ', ' ', ' ', ' '],
        [' ', 'А', ' ', ' ', ' '],
        [' ', ' ', 'Л', ' ', ' '],
        [' ', ' ', ' ', 'Д', ' '],
        [' ', ' ', ' ', ' ', 'А']
    ]
    display_board(test_board)

    r, c, l, wc = get_player_move_input("Тестовый Игрок", 5)
    print(f"Ввод игрока: Новая буква '{l}' в ({r},{c}), слово из координат: {wc}")

    display_message("Какое-то сообщение от игры.")

    test_scores = {1: {'score': 10, 'name': 'Игрок 1'},
                   2: {'score': 7, 'name': 'Игрок 2'}}
    display_scores(test_scores)

    play_again = ask_to_play_again()
    print(f"Сыграть снова: {play_again}")
    print("Тестирование User Interface завершено.")