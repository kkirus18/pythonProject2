"""Главный модуль программы - точка входа."""
import random
import sys
import os

# Добавляем путь к модулям (для корректного импорта)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.quiz_generator import QuizGenerator
from modules.quiz_engine import QuizEngine
from modules.utils import generate_test_id, clear_screen, validate_number_input


def show_menu():
    """Отображение главного меню."""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎓 ГЕНЕРАТОР ТЕСТОВ 🎓                    ║
║                   Система лингвистического                   ║
║                     тестирования v1.0                        ║
╚══════════════════════════════════════════════════════════════╝

📌 Выберите режим работы:

   1. 📚 Режим «ОБУЧЕНИЕ» (с подсказками)
   2. 🎯 Режим «ЭКЗАМЕН» (без подсказок)
   3. ℹ️  Информация о программе
   4. 🚪 Выход

""")


def show_info(generator: QuizGenerator):
    """Отображение информации о программе."""
    clear_screen()
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                     ℹ️ ИНФОРМАЦИЯ                           ║
╚══════════════════════════════════════════════════════════════╝

📋 База вопросов содержит {generator.questions_count} вопросов по:
   • Языкознанию и лингвистике
   • Языковым семьям мира
   • Кодам ISO 639
   • Типологии языков

🎮 Функциональность:
   • Случайная выборка вопросов
   • Перемешивание вариантов ответов
   • Два режима: Экзамен / Обучение
   • Уникальный ID каждого теста
   • Разбор ошибок после завершения

📌 В режиме «Обучение» после неправильного ответа
   показывается подсказка.

🔄 Каждый запуск теста генерирует уникальный порядок
   вопросов и вариантов ответов для каждого пользователя.
""")
    input("\n⏎ Нажмите Enter для возврата в меню...")


def get_question_count(generator: QuizGenerator) -> int:
    """
    Получение от пользователя количества вопросов в тесте.

    Аргументы:
        generator: экземпляр QuizGenerator

    Возвращает:
        количество вопросов
    """
    max_q = generator.questions_count
    print(f"\n📊 Всего в базе: {max_q} вопросов")
    return validate_number_input(
        f"🔢 Сколько вопросов включить в тест? (1-{max_q}): ",
        1, max_q
    )


def run_test():
    """Запуск основного процесса тестирования."""
    generator = QuizGenerator()

    while True:
        clear_screen()
        show_menu()

        choice = validate_number_input("👉 Ваш выбор (1-4): ", 1, 4)

        # ИНИЦИАЛИЗИРУЕМ ПЕРЕМЕННЫЕ ЗНАЧЕНИЯМИ ПО УМОЛЧАНИЮ
        mode = "exam"  # значение по умолчанию
        mode_name = "ЭКЗАМЕН (без подсказок)"  # значение по умолчанию

        if choice == 1:
            # Режим обучения
            mode = "learning"
            mode_name = "ОБУЧЕНИЕ (с подсказками)"
        elif choice == 2:
            # Режим экзамена
            mode = "exam"
            mode_name = "ЭКЗАМЕН (без подсказок)"
        elif choice == 3:
            show_info(generator)
            continue
        elif choice == 4:
            clear_screen()
            print("👋 До свидания! Спасибо за использование генератора тестов!")
            break

        # Генерация уникального теста
        clear_screen()
        print(f"{'=' * 50}")
        print(f"🎓 Запуск теста в режиме: {mode_name}")
        print(f"{'=' * 50}")

        # Получаем количество вопросов
        n_questions = get_question_count(generator)

        # Генерируем уникальный ID теста
        test_id = generate_test_id()
        print(f"\n🆔 Уникальный ID вашего теста: {test_id}")
        print("   (сохраните его для возможности повтора)")

        # Выборка вопросов
        questions = generator.get_random_questions(n_questions)

        # Создаём и запускаем движок
        engine = QuizEngine(questions, mode=mode)
        correct, total, results = engine.run()

        # Показываем результаты
        engine.show_final_score(correct, total, test_id, results)

        print("\n🔄 Выберите действие:")
        print("   1. Пройти тест заново")
        print("   2. Вернуться в главное меню")

        post_choice = validate_number_input("👉 Ваш выбор (1-2): ", 1, 2)

        if post_choice == 2:
            continue
        # Если выбрано 1 - цикл продолжится и начнётся новый тест


def main():
    """Точка входа в программу."""
    random.seed()  # инициализация генератора случайных чисел
    run_test()


if __name__ == "__main__":
    main()