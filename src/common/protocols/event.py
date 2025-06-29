from abc import ABC, abstractmethod
from pydantic import BaseModel


class BaseEvent(ABC):
    @abstractmethod
    async def handle(self, param: type[BaseModel] | None = None) -> None:
        ...
