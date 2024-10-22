from ycappuccino.api.storage import IManager


class Manager(IManager):
    def __init__(self, storage: IStorage):
        self.storage = storage
        self._logger = logging.getLogger(self.__class__.__name__)

    def get(self, key: str) -> Any:
        return self.storage.get(key)

    def set(self, key: str, value: Any) -> None:
        self.storage.set(key, value)

    def delete(self, key: str) -> None:
        self.storage.delete(key)

    def exists(self, key: str) -> bool:
        return self.storage.exists(key)

    def keys(self) -> List[str]:
        return self.storage.keys()

    def values(self) -> List[Any]:
        return self.storage.values()

    def items(self) -> List[Tuple[str, Any]]:
        return self.storage.items()
