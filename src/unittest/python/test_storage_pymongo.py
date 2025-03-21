import pytest
import pytest_asyncio
from pymongo import MongoClient

from ycappuccino.api.base import IActivityLogger, IConfiguration
from ycappuccino.api.storage import FilterTenant, Query
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
    async def setup(
        self,
    ) -> None:
        self.pymongo_storage_adapter = PyMongoStorageAdapter(
            config=FakeConfiguration(),
            logger=FakeLogger(),
        )

    async def test_given_mongo_connected_and_collection_empty_get_one(self) -> None:
        # Given
        await self.pymongo_storage_adapter.connect()
        # When
        result = await self.pymongo_storage_adapter.get_one("test", "test")
        # Then
        assert result is None

    async def test_given_mongo_connected_and_collection_with_elem_get_one(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=["test"]),
            a_new_dict={"name": "test"},
        )

        # When
        result = await self.pymongo_storage_adapter.get_one(
            "test",
            a_id="test",
            a_filter=FilterTenant(tenant=["test"]),
            a_params=Query(offset=0, limit=1, sort=""),
        )
        #
        # Then
        assert result == {"name": "test"}

    async def test_given_mongo_connected_and_collection_with_elem_aggregate(
        self,
    ) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=["test"]),
            a_new_dict={"name": "test"},
        )
        # When
        result = await self.pymongo_storage_adapter.aggregate(
            a_collection="test",
            a_filter=FilterTenant(tenant=["test"]),
            a_pipeline=[{"$match": {"name": "test"}}],
        )

        # Then
        assert result == [{"name": "test"}]

    async def test_given_mongo_connected_and_collection_empty_aggregate(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        # When
        result = await self.pymongo_storage_adapter.aggregate(
            a_collection="test",
            a_filter=FilterTenant(tenant=["test"]),
            a_pipeline=[{"$match": {"name": "test"}}],
        )

        # Then
        assert result == []

    async def test_given_mongo_connected_and_no_collection_get_one(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        # When
        result = await self.pymongo_storage_adapter.get_one(
            a_collection="test", a_id="test", a_filter=FilterTenant(tenant=[])
        )
        # Then
        assert result is None

    async def test_given_mongo_connected_and_collection_get_many(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
            a_new_dict={"name": "test"},
        )
        # When
        result = await self.pymongo_storage_adapter.get_many(
            a_collection="test",
            a_filter=FilterTenant(tenant=[]),
            a_params=Query(offset=0, limit=1, sort=""),
        )
        # Then
        assert result == [{"name": "test"}]

    async def test_given_mongo_connected_and_collection_list(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
            a_new_dict={"name": "test"},
        )
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
            a_new_dict={"name": "test2"},
        )
        # When
        result = await self.pymongo_storage_adapter.get_many(
            a_collection="test",
            a_filter=FilterTenant(tenant=[]),
            a_params=Query(offset=0, limit=2, sort=""),
        )
        # Then
        assert len(result) == 2
        assert result == [{"name": "test"}, {"name": "test2"}]

    async def test_given_mongo_connected_and_collection_insert_one(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        # When
        result = await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
            a_new_dict={"name": "test"},
        )
        # Then
        assert result.acknowledged
        res = await self.pymongo_storage_adapter.get_one(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
        )
        assert res == {"name": "test"}

    async def test_given_mongo_connected_and_collection_insert_many(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        # When
        result = await self.pymongo_storage_adapter.up_sert_many(
            a_collection="test",
            a_filter=FilterTenant(tenant=[]),
            a_list_dict=[{"name": "test"}, {"name": "test2"}],
        )
        # Then
        assert result.acknowledged
        res = await self.pymongo_storage_adapter.get_one(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
        )
        assert res == {"name": "test", "name2": "test2"}

    async def test_given_mongo_connected_and_collection_delete_one(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
        )
        # When
        result = await self.pymongo_storage_adapter.delete(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
        )
        # Then
        assert result.acknowledged
        res = await self.pymongo_storage_adapter.get_one("test")
        assert res is None

    async def test_given_mongo_connected_and_collection_delete_many(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
            a_new_dict={"name": "test"},
        )
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
            a_new_dict={"name": "test2"},
        )
        # When
        result = await self.pymongo_storage_adapter.delete_many(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
        )
        # Then
        assert result.acknowledged
        res = await self.pymongo_storage_adapter.get_many(
            a_collection="test",
            a_filter=FilterTenant(tenant=[]),
        )
        assert res == []

    async def test_given_mongo_connected_and_collection_update_one(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test", a_filter=None, a_new_dict={"name": "test"}
        )
        # When
        result = await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
            a_new_dict={"name": "test2"},
        )
        # Then
        assert result.acknowledged
        res = await self.pymongo_storage_adapter.get_one(
            a_collection="test",
            a_id="test",
            a_filter=FilterTenant(tenant=[]),
        )
        assert res == {"name": "test2"}

    async def test_given_mongo_connected_and_collection_update_many(self) -> None:

        # Given
        await self.pymongo_storage_adapter.connect()
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="id_test",
            a_filter=FilterTenant(tenant=[]),
            a_new_dict={"name": "test"},
        )
        await self.pymongo_storage_adapter.up_sert(
            a_collection="test",
            a_id="id_test",
            a_filter=FilterTenant(tenant=[]),
            a_new_dict={"name": "test2"},
        )
        # When
        result = await self.pymongo_storage_adapter.up_sert_many(
            a_collection="test",
            a_filter=FilterTenant(tenant=[]),
            a_list_dict=[{"name": "test3"}],
        )
        # Then
        assert result.acknowledged
        res = await self.pymongo_storage_adapter.get_many(
            a_collection="test",
            a_filter=FilterTenant(tenant=[]),
        )
        assert res == [{"name": "test3"}, {"name": "test3"}]
