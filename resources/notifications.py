from .base import Base


class Notifications(Base):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__, 'NotificationsArchive')
