import logging
from typing import List

from rich.logging import RichHandler

from .models import DataModel

logging.basicConfig(level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Base:
    __base_url = 'https://gu.ac.ir/'

    def __init__(self, name: str, section_url: str) -> None:
        self._name = name
        self._section_url = section_url

    def get_latest(self) -> DataModel:
        raise NotImplementedError

    def get_all(self, page: int = 1) -> List[DataModel]:
        raise NotImplementedError

    def log(self, level: int, message: str, *args, **kwargs) -> None:
        message = f'{self._name} | {message}'
        logger.log(level, message, *args, **kwargs)
