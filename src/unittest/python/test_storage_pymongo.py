import pytest
import pytest_asyncio
from pymongo import MongoClient

from ycappuccino.api.base import IActivityLogger, IConfiguration
from ycappuccino.storage.adapter.pymongo_storage_adapter import PyMongoStorageAdapter


class FakeConfiguration(IConfiguration):

    async def start(self):
        pass

    async def stop(self):
        pass


class FakeLogger(IActivityLogger):
    async def start(self):
        pass

    async def stop(self):
        pass


@pytest.mark.asyncio
class TestPyMongoStorage:

    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, _mongo_client_factory: type[MongoClient]) -> None:
        self._mongo_client_factory = _mongo_client_factory
        self.pymongo_storage_adapter = PyMongoStorageAdapter(
            config=FakeConfiguration(),
            logger=FakeLogger(),
            mongo_client_type=self._mongo_client_factory,
        )

    async def test_given_mongo_connected_and_collection_empty_get_one(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_with_elem_get_one(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_with_elem_aggregate(
        self,
    ) -> None:

        pass

    async def test_given_mongo_connected_and_collection_empty_aggregate(self) -> None:

        pass

    async def test_given_mongo_connected_and_no_collection_get_one(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_get_many(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_list(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_insert_one(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_insert_many(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_delete_one(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_delete_many(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_update_one(self) -> None:

        pass

    async def test_given_mongo_connected_and_collection_update_many(self) -> None:

        pass
