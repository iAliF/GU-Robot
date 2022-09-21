from typing import List

from .models import DataModel


class Base:
    __base_url = 'https://gu.ac.ir/'

    def __init__(self, section_url: str) -> None:
        self._section_url = section_url

    def get_latest(self) -> DataModel:
        raise NotImplementedError

    def get_all(self, page: int = 1) -> List[DataModel]:
        raise NotImplementedError
