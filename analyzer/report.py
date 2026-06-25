"""
Файл для создания отчета по собранной статистике
"""


from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from analyzer.models import Statistics


class ReportBuilder:

    def __init__(self):
        pass

    @staticmethod
    def build(
        output_file: str,
        stats: Statistics,
        invalid_lines: list,
    ):
        """
        Собираем статистику в отчет по шаблону
        :param output_file:  Имя выходного файла
        :param stats: Статистика по логам
        :param invalid_lines: Ошибочные строки
        :return: None
        """

        env = Environment(loader=FileSystemLoader("templates"))             # Подгружаем папку с шаблонами
        template = env.get_template("report.html.j2")                       # Получаем шаблон
        html = template.render(stats=stats, invalid_lines=invalid_lines)    # Рендерим отчет
        Path(output_file).write_text(html, encoding="utf-8")                # Сохраняем отчет
