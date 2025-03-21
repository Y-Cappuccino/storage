import asyncio
import json
import time
from uuid import uuid4
import typing as t
from pymongo import AsyncMongoClient, MongoClient

from ycappuccino.api.base import IActivityLogger, IConfiguration
from ycappuccino.api.executor_service import RunnableProcess
from ycappuccino.api.storage import FilterTenant, IStorage, Query
from ycappuccino.api import executor_service


class ValidateStorageConnect(RunnableProcess):
    """ """

    def __init__(self, a_service):
        super(ValidateStorageConnect, self).__init__("validateStorageConnect")
        self._service = a_service

    def process(self):
        asyncio.run(self._service.validateConnect())


class FakeMongoClient(MongoClient):
    def __init__(self, *args, **kwargs):
        pass

    def server_info(self):
        pass


class PyMongoStorageAdapter(IStorage):

    async def aggregate(
        self,
        a_collection: str,
        a_filter: FilterTenant,
        a_pipeline: t.List[t.Dict[str, t.Any]],
    ):
        pass

    async def get_one(
        self, a_collection: str, a_id: str, a_filter: FilterTenant, a_params: Query
    ):
        pass

    async def get_many(
        self, a_collection: str, a_filter: FilterTenant, a_params: Query
    ):
        pass

    async def up_sert(
        self,
        a_collection: str,
        a_id: str,
        a_filter: FilterTenant,
        params: Query,
        a_new_dict: t.Dict[str, t.Any],
    ):
        pass

    async def up_sert_many(
        self,
        a_collection: str,
        a_filter: FilterTenant,
        params: Query,
        a_list_dict: t.List[t.Dict[str, t.Any]],
    ):
        pass

    async def delete(
        self, a_collection: str, a_id: str, a_filter: FilterTenant, query: Query
    ):
        pass

    async def delete_many(
        self, a_collection: str, a_filter: FilterTenant, query: Query
    ):
        pass

    def __init__(
        self,
        config: IConfiguration,
        logger: IActivityLogger,
    ) -> None:
        super().__init__()
        self._logger = logger
        self._config = config

        self._db = None
        self._host = "localhost"
        self._port = 27017
        self._username = "client_pyscript_core"

        self._password = "ycappuccino"
        self._db_name = "ycappuccino"
        self._client = None

    async def connect(self):
        self._client = MongoClient(self._host, int(self._port))
        self._db = self._client[self._db_name]

    async def load_configuration(self):
        self._host = self._config.get("storage.mongo.db.host", "localhost")
        self._port = self._config.get("storage.mongo.db.port", 27017)
        self._username = self._config.get(
            "storage.mongo.db.username", "client_pyscript_core"
        )
        self._password = self._config.get("storage.mongo.db.password", "ycappuccino")
        self._db_name = self._config.get("storage.mongo.db.name", "ycappuccino")

    async def start(self):
        self._logger.info("MongoStorage validating")
        try:
            await self.load_configuration()
            await self.connect()
            _threadExecutor = executor_service.new_executor("validateConnectionStorage")
            _callable = ValidateStorageConnect(self)
            _callable.set_activate(True)
            _threadExecutor.submit(_callable)

        except Exception as e:
            self._logger.error("MongoStorage Error {}".format(e))
            self._logger.exception(e)

        self._logger.info("MongoStorage validated")

    async def stop(self):
        self._logger.info("MongoStorage invalidating")
        try:
            if self._client is not None:
                self._client.close()
                self._client = None
                self._db = None
        except Exception as e:
            self._logger.error("MongoStorage Error {}".format(e))
            self._logger.exception(e)
        self._logger.info("MongoStorage invalidated")
