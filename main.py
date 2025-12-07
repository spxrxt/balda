from game_logic import BaldaGame
from user_interface import (
    display_welcome_message,
    get_game_mode,
    display_board,
    get_player_move_input,
    display_message,
    display_scores,
    ask_to_play_again
)
from computer_player import ComputerPlayer


def run_player_vs_player(game):
    """Режим игры: Игрок против Игрока."""
    while True:
        display_board(game.get_board())
        display_scores(game.players)

        player_name = game.get_current_player_name()
        display_message(f"Ход игрока {player_name}.")

        row, col, letter, word_coords = get_player_move_input(player_name, game.board_size)

        # Временная логика, если пользователь не ввел координаты слова, хотя он должен
        if not word_coords:
            display_message("Вы не указали координаты слова. Попробуйте еще раз.")
            continue

        move_successful, message = game.make_move(row, col, letter, word_coords)
        display_message(message)

        if move_successful:
            game.switch_player()

        # Проверка на конец игры (например, нет пустых клеток или нет возможных ходов)
        # Для простоты: игра продолжается, пока кто-то не устанет.
        # В реальной Балде есть правила завершения.
        if not ask_to_play_again():  # Здесь спрашиваем, хочет ли игрок продолжить игру (а не сыграть заново)
            break

    display_message("Игра завершена. Итоговые очки:")
    display_scores(game.players)


def run_player_vs_computer(game):
    """Режим игры: Игрок против Компьютера."""
    computer_player = ComputerPlayer(game)

    while True:
        display_board(game.get_board())
        display_scores(game.players)

        if game.current_player_id == 1:  # Ход человека
            player_name = game.get_current_player_name()
            display_message(f"Ход игрока {player_name}.")
            row, col, letter, word_coords = get_player_move_input(player_name, game.board_size)

            if not word_coords:
                display_message("Вы не указали координаты слова. Попробуйте еще раз.")
                continue

            move_successful, message = game.make_move(row, col, letter, word_coords)
            display_message(message)

            if move_successful:
                game.switch_player()
            else:
                # Если ход человека не удался, даем ему еще попытку
                display_message("Пожалуйста, попробуйте еще раз.")
                continue

        else:  # Ход компьютера
            display_message("Ход компьютера...")
            ai_success, letter, r, c, word, score = computer_player.make_computer_move()

            if ai_success:
                display_message(
                    f"Компьютер поставил '{letter}' в ({r},{c}) и составил слово '{word}' (+{score} очков).")
                game.switch_player()
            else:
                display_message("Компьютер не смог найти ход. Вы выиграли!")
                break  # Компьютер не может ходить, игра окончена

        if not ask_to_play_again():  # Здесь спрашиваем, хочет ли игрок продолжить игру (а не сыграть заново)
            break

    display_message("Игра завершена. Итоговые очки:")
    display_scores(game.players)


def main():
    """Главная функция для запуска игры Балда."""

    display_welcome_message()

    while True:
        game_mode = get_game_mode()

        # Создаем новый экземпляр игры для каждого нового раунда
        game = BaldaGame(board_size=5, initial_word="БАЛДА")  # Можно передавать путь к словарю

        if game_mode == "player_vs_player":
            game.players[1]['name'] = input("Имя Игрока 1: ") or "Игрок 1"
            game.players[2]['name'] = input("Имя Игрока 2: ") or "Игрок 2"
            run_player_vs_player(game)
        elif game_mode == "player_vs_computer":
            game.players[1]['name'] = input("Ваше имя: ") or "Игрок"
            game.players[2]['name'] = "Компьютер"
            run_player_vs_computer(game)

        if not ask_to_play_again():  # Здесь спрашиваем, хочет ли пользователь начать новую игру
            break

    display_message("Спасибо за игру в Балду!")


if __name__ == "__main__":
    main()