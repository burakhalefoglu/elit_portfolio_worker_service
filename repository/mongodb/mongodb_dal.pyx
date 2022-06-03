import os

import motor.motor_asyncio
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()
cdef str mongodb_connection = os.getenv('MONGODB')

cdef class MongodbDal:
    client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_connection)
    db = client["elitdb"]

    async def get_transaction_session_async(self):
        return await self.client.start_session()

    async def add_async(self, str table, object model):
        col = self.db[table]
        session = await self.get_transaction_session_async()
        m = model
        if type(model) is not dict:
            m = model.__dict__
        x = await col.insert_one(m, session=session)
        return x.inserted_id

    async def add_many_async(self, str table, list models):
        col = self.db[table]
        await col.insert_many(models)

    async def get_all_with_client_id_async(self, str table, str client_id):
        col = self.db[table]
        cursor = col.find({"client_id": client_id, "status": True})
        return await cursor.to_list(length=1000)

    async def get_by_id_async(self, str table, str _id, str client_id):
        col = self.db[table]
        model = await col.find_one({"_id": ObjectId(_id), "client_id": client_id, "status": True})
        self.client.close()
        return model

    async def get_all_async(self, str table):
        col = self.db[table]
        cursor = col.find({"status": True})
        return await cursor.to_list(length=10000)

    async def get_by_filter_async(self, str table, dict filters):
        self.__reformat_id_if_exist(filters)
        col = self.db[table]
        model = await col.find_one(filters)
        return model

    async def get_list_by_filter_async(self, str table, dict filters):
        self.__reformat_id_if_exist(filters)
        col = self.db[table]
        cursor = col.find(filters)
        return await cursor.to_list(length=10000)

    async def update_async(self, str table, dict query, dict new_value):
        self.__reformat_id_if_exist(query)
        col = self.db[table]
        return await col.update_one(query, {"$set": new_value}, upsert=False)

    async def delete_async(self, str table, dict query):
        self.__reformat_id_if_exist(query)
        col = self.db[table]
        result = await col.update_one(
            query, {"$set": {"status": False}}, upsert=False)
        return result.raw_result

    async def delete_all_async(self, str table, dict query):
        self.__reformat_id_if_exist(query)
        col = self.db[table]
        await col.update_many(query, {"$set": {"status": False}}, upsert=False)

    def __reformat_id_if_exist(self, query):
        if '_id' in query:
            query['_id'] = ObjectId(query['_id'])
