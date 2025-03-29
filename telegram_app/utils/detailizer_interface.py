from abc import ABC, abstractmethod

from orm.models import Games, Event


class IDetailizer(ABC):
    @abstractmethod
    def prepare_message_text(self, obj: (Games, Event)) -> str:
        pass

    @abstractmethod
    def prepare_message_files(self, game: (Games, Event), message_text: str) -> list:
        pass
