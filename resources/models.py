from dataclasses import dataclass


@dataclass
class Item:
    title: str
    url: str
    date: str
    image_url: str

    def __str__(self) -> str:
        return f'{self.title} - {self.date}'
