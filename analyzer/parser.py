"""
Класс парсинга логов
"""

from datetime import datetime

from loguru import logger

from analyzer.models import LogRecord
from analyzer.settings import LOG_PATTERN


class LogParser:

    @staticmethod
    def parse(
        line: str,
        filename: str,
    ) -> LogRecord | None:
        """
        Парсим строку по шаблону
        :param line:
        :param filename:
        :return:
        """

        match = LOG_PATTERN.match(line.strip())             # Парсим строку по шаблону

        if not match:
            return None

        try:

            # Преобразуем строку в объект datetime
            timestamp = datetime.strptime(
                f"{match.group('date')} {match.group('time')}",
                "%Y-%m-%d %H:%M:%S",
            )

            return LogRecord(
                timestamp=timestamp,
                level=match.group("level"),
                message=match.group("message"),
                filename=filename,
            )

        except ValueError:
            return None

        except Exception as e:
            logger.error(f"Непредвиденная ошибка", exception=e)
            return None
