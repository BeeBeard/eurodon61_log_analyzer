"""
Класс для подсчета статистики по логам
"""


from collections import Counter, defaultdict

from analyzer.models import FileStatistics, LogRecord, Statistics
from analyzer.settings import DEFAULT_PROBLEM_LEVELS


class StatBuilder:

    def __init__(self):
        pass

    @staticmethod
    def build(records: list[LogRecord]) -> Statistics:
        """
        Подсчет статистики по логам
        :param records:
        :return:
        """

        level_counter = Counter()                       # Счетчик уровней
        top_errors = Counter()                          # Счетчик ошибок
        file_stats = defaultdict(FileStatistics)

        for record in records:

            level_counter[record.level] += 1
            stat = file_stats[record.filename]
            stat.total += 1

            #  Подсчет статистики
            match record.level:
                case "INFO":
                    stat.info += 1

                case "WARNING":
                    stat.warning += 1

                case "ERROR":
                    stat.error += 1

                case "CRITICAL":
                    stat.critical += 1

                case "TIMEOUT":
                    stat.timeout += 1

            # Подсчет по указанным уровням ошибок
            if record.level in DEFAULT_PROBLEM_LEVELS:
                top_errors[record.message] += 1

        return Statistics(
            total=len(records),

            info=level_counter.get("INFO"),
            warning=level_counter.get("WARNING"),
            error=level_counter.get("ERROR"),
            critical=level_counter.get("CRITICAL"),
            timeout=level_counter.get("TIMEOUT"),

            top_errors=top_errors.most_common(10),
            files=dict(file_stats),
        )
