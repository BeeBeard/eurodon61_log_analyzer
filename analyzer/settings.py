"""
Файл конфигурации поиска по регулярному выражению
"""

import re


# Паттерн регулярного выражения
LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2}) "
    r"(?P<time>\d{2}:\d{2}:\d{2}) "
    r"(?P<level>[A-Z]+) "
    r"(?P<message>.+)$"
)


# Уровни событий для суммирования по умолчанию
DEFAULT_PROBLEM_LEVELS = {
    "ERROR",
    "CRITICAL",
    "TIMEOUT",
}
