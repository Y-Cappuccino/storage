import logging

from ycappuccino.api.base import IActivityLogger
from ycappuccino.api.storage import IManager, IStorage
import typing as t


class Manager(IManager):
    def __init__(self, storage: IStorage, logger: IActivityLogger):
        self.storage = storage
        self.logger = logger

    def get(self, type_id: str, key: str) -> t.Any: ...

    def set(self, type_id: str, key: str, value: t.Any) -> None: ...

    def delete(self, type_id: str, key: str) -> None: ...

    def exists(self, type_id: str, key: str) -> bool: ...

    def keys(self, type_id: str) -> t.List[str]: ...
