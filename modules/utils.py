"""Утилиты для работы теста."""
import random
import datetime
import os
import sys

def generate_test_id() -> str:
    """
    Генерация уникального ID теста.

    Формат: YYYYMMDD_HHMMSS_XXXX
    - Дата и время текущего момента
    - 4 случайных символа (буквы/цифры)
    """
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    random_suffix = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
    return f"{timestamp}_{random_suffix}"


def clear_screen():
    """Очистка экрана терминала (кроссплатформенная)."""
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


def validate_number_input(prompt: str, min_val: int, max_val: int) -> int:
    """
    Ввод и валидация числа от пользователя.

    Аргументы:
        prompt: текст приглашения
        min_val: минимальное допустимое значение
        max_val: максимальное допустимое значение

    Возвращает:
        валидное число
    """
    while True:
        try:
            user_input = input(prompt)
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"⚠️  Введите число от {min_val} до {max_val}")
        except ValueError:
            print("⚠️  Пожалуйста, введите целое число")