import json

from dataclasses import dataclass
from typing import Dict


@dataclass
class Config:
    """Класс для хранения конфигурации приложения"""
    PATHS: Dict[str, str]
    AES_KEY_SIZE: int = 256

    @classmethod
    def from_json(cls, config_path: str) -> 'Config':
        """Загружает конфигурацию из JSON файла"""
        with open(config_path) as f:
            return cls(PATHS=json.load(f))