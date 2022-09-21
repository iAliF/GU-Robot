from .base import Base


class News(Base):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__, 'NewsArchive')
