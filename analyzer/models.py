"""
Модели для работы с данными
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field

from analyzer.settings import DEFAULT_PROBLEM_LEVELS


class LogRecord(BaseModel):
    model_config = ConfigDict(frozen=True)
    timestamp: datetime
    level: str
    message: str
    filename: str


class InvalidLogLine(BaseModel):
    model_config = ConfigDict(frozen=True)
    filename: str
    line_number: int
    content: str


class FileStatistics(BaseModel):
    total: int = 0
    info: int = 0
    warning: int = 0
    error: int = 0
    critical: int = 0
    timeout: int = 0


class Statistics(BaseModel):
    total: int
    info: int
    warning: int
    error: int
    critical: int
    timeout: int
    top_errors: list[tuple[str, int]]
    files: dict[str, FileStatistics]

    # Расчет количества проблемных событий по уровням из settings
    @computed_field
    @property
    def problem_events(self) -> int:
        return sum(
            getattr(self, level.lower(), 0)
            for level in DEFAULT_PROBLEM_LEVELS
        )

    # Расчет уровней проблемных событий
    @computed_field
    @property
    def problem_levels(self) -> str:
        return ", ".join(DEFAULT_PROBLEM_LEVELS)
