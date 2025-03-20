import asyncio
import json
import time
from uuid import uuid4
import typing as t
from pymongo import AsyncMongoClient, MongoClient

from ycappuccino.api.base import IActivityLogger, IConfiguration
from ycappuccino.api.executor_service import RunnableProcess
from ycappuccino.api.storage import Filter, IStorage, Query
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

    def __init__(
        self,
        config: IConfiguration,
        logger: IActivityLogger,
        mongo_client_type: type[MongoClient] = MongoClient,
    ) -> None:
        super().__init__()
        self._logger = logger
        self._config = config
        self._mongo_client_type = mongo_client_type

        self.mongo_client = None
        self._db = None
        self._host = "localhost"
        self._port = 27017
        self._username = "client_pyscript_core"

        self._password = "ycappuccino"
        self._db_name = "ycappuccino"
        self._client = None

    async def connect(self):
        self._client = self._mongo_client_type(self._host, int(self._port))
        self._db = self._client[self._db_name]

    async def load_configuration(self):
        self._host = self._config.get("storage.mongo.db.host", "localhost")
        self._port = self._config.get("storage.mongo.db.port", 27017)
        self._username = self._config.get(
            "storage.mongo.db.username", "client_pyscript_core"
        )
        self._password = self._config.get("storage.mongo.db.password", "ycappuccino")
        self._db_name = self._config.get("storage.mongo.db.name", "ycappuccino")

    async def aggregate(
        self, a_collection: str, a_pipeline: t.List[t.Dict[str, t.Any]]
    ):
        """aggegate data regarding filter and pipeline"""
        pass
        # return self._db[a_collection].aggregate(a_pipeline)

    async def get_one(
        self, a_collection: str, a_filter: Filter = None, a_params: Query = None
    ):
        """get dict identify by a Id"""
        return self._db[a_collection].find(a_filter)

    async def get_many(
        self, a_collection: str, a_filter: Filter, a_params: Query = None
    ) -> t.List[t.Dict[str, t.Any]]:
        """return iterable of dict regarding filter"""
        w_offset = 0
        w_limit = 50
        w_sort: t.Dict[str, t.Any] = {"_cat": -1}

        if a_params.offset is not None:
            w_offset = a_params.offset
        if a_params.limit is not None:
            w_limit = a_params.limit
        if a_params.sort is not None:
            w_sort = json.loads(a_params.sort)

        w_res = self._db[a_collection].find(a_filter)
        w_res = w_res.sort(w_sort.items())
        w_res = w_res.skip(w_offset)
        w_res = w_res.limit(w_limit)

        return w_res

    async def up_sert(
        self,
        a_collection: str,
        a_id: str,
        a_filter: Filter,
        a_new_dict: t.Dict[str, t.Any],
    ):
        """ " update or insert new dict"""

        return self._db[a_collection].update_one({"_id": a_id}, a_new_dict, upsert=True)

    async def up_sert_many(
        self,
        a_collection: str,
        a_filter: Filter,
        a_list_dict: t.List[t.Dict[str, t.Any]],
    ):
        """update or insert document with new dict regarding filter"""

        return self._db[a_collection].update_many(a_filter, a_list_dict, upsert=True)

    async def delete(self, a_collection, a_id):
        """delete document identified by id if it exists"""
        w_filter = {"_id": a_id}
        self._db[a_collection].delete_one(w_filter, upsert=True)

    async def delete_many(self, a_collection, a_filter):
        self._db[a_collection].delete_many(a_filter, upsert=True)

    async def validateConnect(self):
        """ """
        try:
            self._client.server_info()
            self._available = True
        except Exception as e:
            self._available = False

    async def start(self):
        self._logger.info("MongoStorage validating")
        try:
            await self.load_configuration()
            self._client = self._mongo_client_type(self._host, int(self._port))
            self._db = self._client[self._db_name]
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
