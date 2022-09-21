from dataclasses import dataclass


@dataclass
class Item:
    title: str
    url: str
    date: str
    image_url: str
