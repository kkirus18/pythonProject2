"""Движок тестирования: приём ответов, подсчёт результатов, режимы."""
import random
from typing import List, Dict, Any, Tuple
from .utils import clear_screen, validate_number_input


class QuizEngine:
    """Движок проведения тестирования."""

    def __init__(self, questions: List[Dict[str, Any]], mode: str = "exam"):
        """
        Инициализация движка.

        Аргументы:
            questions: список вопросов для теста
            mode: режим работы ('exam' - экзамен, 'learning' - обучение)
        """
        self.original_questions = questions
        self.mode = mode
        self.shuffled_questions = []  # будет заполнен при prepare()
        self.results = []  # список словарей с результатами по каждому вопросу

    def prepare(self):
        """
        Подготовка теста: перемешивание вопросов и вариантов ответов.
        Создаёт уникальный порядок для каждого запуска.
        """
        from .quiz_generator import QuizGenerator
        generator = QuizGenerator()

        # Перемешиваем вопросы
        self.shuffled_questions = random.sample(self.original_questions, len(self.original_questions))

        # Для каждого вопроса перемешиваем варианты ответов
        self.mapping_info = []  # храним маппинги для каждого вопроса
        shuffled_with_options = []

        for q in self.shuffled_questions:
            shuffled_q, mapping = generator.shuffle_options(q)
            shuffled_with_options.append(shuffled_q)
            self.mapping_info.append(mapping)

        self.shuffled_questions = shuffled_with_options

    def display_question(self, q: Dict[str, Any], q_num: int, total: int):
        """
        Отображение вопроса и вариантов ответов.

        Аргументы:
            q: словарь с вопросом
            q_num: номер вопроса (с 1)
            total: общее количество вопросов
        """
        print(f"\n📌 Вопрос {q_num}/{total}")
        print(f"📝 {q['question']}")
        print("\n   Варианты ответов:")

        for i, option in enumerate(q["options"], start=1):
            print(f"   {i}. {option}")

        print()

    def get_user_answer(self, q: Dict[str, Any]) -> int:
        """
        Получение ответа от пользователя с валидацией.

        Аргументы:
            q: словарь с вопросом

        Возвращает:
            номер выбранного варианта (0-based индекс)
        """
        num_options = len(q["options"])
        # Пользователь видит варианты с 1, поэтому преобразуем
        choice = validate_number_input(
            f"🔢 Ваш ответ (1-{num_options}): ",
            1, num_options
        )
        return choice - 1  # преобразуем в 0-based индекс

    def show_feedback(self, is_correct: bool, correct_answer: str, hint: str = None):
        """
        Отображение обратной связи после ответа.

        Аргументы:
            is_correct: правильность ответа
            correct_answer: текст правильного ответа
            hint: подсказка (для режима обучения)
        """
        if is_correct:
            print("\n✅ Правильно!")
        else:
            print(f"\n❌ Неправильно. Правильный ответ: {correct_answer}")
            if self.mode == "learning" and hint:
                print(f"💡 Подсказка: {hint}")
        print("\n" + "-" * 50)

    def run(self) -> Tuple[int, int, List[Dict[str, Any]]]:
        """
        Запуск тестирования.

        Возвращает:
            кортеж (количество_правильных, общее_количество, детальные_результаты)
        """
        self.prepare()
        total = len(self.shuffled_questions)
        correct_count = 0

        for idx, q in enumerate(self.shuffled_questions):
            clear_screen()
            print(f"{'=' * 50}")
            print(f"🎓 РЕЖИМ: {'ЭКЗАМЕН' if self.mode == 'exam' else 'ОБУЧЕНИЕ (с подсказками)'}")
            print(f"📊 Прогресс: {idx}/{total} вопросов пройдено")
            print(f"{'=' * 50}")

            self.display_question(q, idx + 1, total)
            user_choice = self.get_user_answer(q)

            is_correct = (user_choice == q["correct"])

            if is_correct:
                correct_count += 1

            self.show_feedback(
                is_correct=is_correct,
                correct_answer=q["options"][q["correct"]],
                hint=q.get("hint")
            )

            # Сохраняем результат
            self.results.append({
                "question": q["question"],
                "user_choice": user_choice,
                "user_choice_text": q["options"][user_choice],
                "correct": q["correct"],
                "correct_text": q["options"][q["correct"]],
                "is_correct": is_correct,
                "hint": q.get("hint")
            })

            if idx < total - 1:
                input("⏎ Нажмите Enter для продолжения...")

        return correct_count, total, self.results

    def show_final_score(self, correct: int, total: int, test_id: str, results: List[Dict[str, Any]]):
        """
        Отображение финального результата с разбором ошибок.

        Аргументы:
            correct: количество правильных ответов
            total: общее количество вопросов
            test_id: уникальный ID теста
            results: детальные результаты
        """
        clear_screen()
        percentage = (correct / total) * 100

        print(f"{'=' * 60}")
        print(f"🎯 РЕЗУЛЬТАТЫ ТЕСТА")
        print(f"{'=' * 60}")
        print(f"🆔 ID теста: {test_id}")
        print(f"📋 Режим: {'Экзамен' if self.mode == 'exam' else 'Обучение'}")
        print(f"📊 Верных ответов: {correct} из {total}")
        print(f"📈 Процент: {percentage:.1f}%")

        # Оценка по 5-балльной шкале
        if percentage >= 90:
            grade = "5 (отлично)"
        elif percentage >= 70:
            grade = "4 (хорошо)"
        elif percentage >= 50:
            grade = "3 (удовлетворительно)"
        else:
            grade = "2 (неудовлетворительно)"

        print(f"🎓 Оценка: {grade}")
        print(f"{'=' * 60}")

        # Разбор ошибок
        errors = [r for r in results if not r["is_correct"]]
        if errors:
            print(f"\n📖 РАЗБОР ОШИБОК ({len(errors)} ошибок):")
            print("-" * 50)
            for i, err in enumerate(errors, 1):
                print(f"\n{i}. Вопрос: {err['question']}")
                print(f"   ❌ Ваш ответ: {err['user_choice_text']}")
                print(f"   ✅ Правильный ответ: {err['correct_text']}")
                if self.mode == "learning" and err.get("hint"):
                    print(f"   💡 Подсказка: {err['hint']}")
        else:
            print(f"\n🏆 Поздравляем! Вы ответили правильно на все вопросы!")

        print(f"\n{'=' * 60}")