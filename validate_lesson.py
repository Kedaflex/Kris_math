import re
import sys

def validate_lesson(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []
    warnings = []

    # Check required headings/sections
    required_sections = [
        ("Тема:", "Тема урока"),
        ("Класс:", "Класс"),
        ("Продолжительность:", "Продолжительность"),
        ("Оборудование и материалы:", "Оборудование и материалы"),
        ("Цель урока:", "Цель урока"),
        ("Задачи урока:", "Задачи урока"),
        ("Ключевые понятия:", "Ключевые понятия"),
        ("Подробный хронометраж", "Таблица хронометража"),
        ("ПОДРОБНЫЙ СЦЕНАРИЙ ДЛЯ УЧИТЕЛЯ", "Сценарий для учителя"),
        ("Итог урока", "Итог урока"),
        ("Рефлексия", "Рефлексия"),
        ("Форма контроля", "Форма контроля"),
        ("КРАТКАЯ МЕТОДИЧЕСКАЯ СТРУКТУРА", "Краткая методическая структура")
    ]

    for req, name in required_sections:
        if req.lower() not in content.lower():
            errors.append(f"Отсутствует обязательная секция/поле: {name} ('{req}')")

    # Check table timing total
    # Timing table typically has rows like: | 0–3 мин | ... | ... | or | 3-8 мин | ... |
    # Or intervals like 0-3, 3-10, 10-25, etc.
    intervals = re.findall(r'(\d+)\s*[\u2013\u2014\-]\s*(\d+)\s*мин', content)
    if intervals:
        total_time = 0
        last_end = 0
        for start_str, end_str in intervals:
            start, end = int(start_str), int(end_str)
            duration = end - start
            total_time += duration
            last_end = max(last_end, end)
        print(f"Найденные интервалы времени: {intervals}")
        print(f"Итоговая продолжительность по хронометражу: {last_end} минут (сумма интервалов: {total_time} мин)")
        if last_end != 45:
            errors.append(f"Общий хронометраж составляет {last_end} минут, ожидается 45 минут!")
    else:
        errors.append("Не удалось распарсить интервалы времени из таблицы хронометража.")

    if errors:
        print("ОШИБКИ ВАЛИДАЦИИ:")
        for err in errors:
            print(f"- {err}")
        return False
    else:
        print("Валидация успешно пройдена!")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python validate_lesson.py <путь_к_файлу_урока>")
        sys.exit(1)
    file_path = sys.argv[1]
    success = validate_lesson(file_path)
    if not success:
        sys.exit(1)
