"""
Класс для чтения логов из директории
"""

from pathlib import Path
from typing import List, Tuple

from loguru import logger

from analyzer.models import InvalidLogLine, LogRecord
from analyzer.parser import LogParser


class LogReader:

    def __init__(self) -> None:
        pass

    @staticmethod
    def __get_log_files(logs_path: Path) -> List[Path]:
        if not logs_path.exists():
            raise FileNotFoundError(f"Директория не существует: {logs_path}")

        if not logs_path.is_dir():
            raise NotADirectoryError(f"Путь не является директорией: {logs_path}")

        log_files = list(logs_path.glob("*.log"))

        if not log_files:
            raise ValueError(f"Нет .log файлов в директории: {logs_path}")

        return log_files

    def read_path(
        self,
        logs_path: Path,
    ) -> Tuple[List[LogRecord], List[InvalidLogLine]]:
        """
        Читаем директорию с *.log файлами
        :param logs_path:
        :return:
        """

        records = []
        invalid_lines = []
        log_files = self.__get_log_files(logs_path)

        for file_path in log_files:        # Проходим по всем *.log файлам в директории
            self.__read_file(
                file_path,
                records,
                invalid_lines,
            )

        return records, invalid_lines

    @staticmethod
    def __read_file(
        file_path: Path,
        records: List[LogRecord],
        invalid_lines: List[InvalidLogLine],
    ):
        """
        Чтение файла построчно для анализа и распределение на корректные и некорректные строки
        :param file_path: Путь к папке с *.log файлами
        :param records: Все корректные записи
        :param invalid_lines: Все неверные строки (не распарсились или ошибки в них)
        :return:
        """

        try:
            # Открытие файла
            with file_path.open(encoding="utf-8", errors="ignore") as file:

                # Проходим по всем строкам в файле
                for line_number, line in enumerate(file, start=1):

                    # Парсим строку
                    record = LogParser.parse(
                        line=line,
                        filename=file_path.name,
                    )

                    # Фильтруем на корректные записи
                    if record:
                        records.append(record)
                    else:
                        invalid_lines.append(
                            InvalidLogLine(
                                filename=file_path.name,
                                line_number=line_number,
                                content=line.strip(),
                            )
                        )

        except OSError as e:
            logger.error(f"Невозможно открыть файл по пути: {file_path}: {e}")

        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {file_path}: {e}")
