import argparse
from pathlib import Path

from loguru import logger

from analyzer.reader import LogReader
from analyzer.report import ReportBuilder
from analyzer.stats import StatBuilder


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--logs", required=True)                # Обязательные аргументы (путь к логам)
    parser.add_argument("--output", default="report.html")      # Путь для отчета

    return parser.parse_args()


def main():

    args = parse_args()                                         # Парсим аргументы
    logs_path = Path(args.logs)                                 # Получаем путь к директории

    reader = LogReader()                                        # Создаем экземпляр LogReader
    records, invalid_lines = reader.read_path(logs_path)        # Читаем директорию logs_path

    stat_builder = StatBuilder()                                # Создаем экземпляр StatisticsService
    stats = stat_builder.build(records)                         # Собираем статистику

    # Собираем отчет
    ReportBuilder().build(
        output_file=args.output,
        stats=stats,
        invalid_lines=invalid_lines,
    )

    logger.info(f"Отчет сохранен в {args.output}")


if __name__ == "__main__":
    main()
