from motor.motor_asyncio import AsyncIOMotorClient

class MongoDBClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, uri="mongodb://localhost:27017", db_name="ds_api"):
        if not hasattr(self, 'initialized'):
            self.uri = uri
            self.db_name = db_name
            self.client = None
            self.db = None
            self.initialized = True
            self.connect()

    def connect(self):
        if not self.client:
            print("Connecting to MongoDB...")
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client[self.db_name]
            print("Mongo Connected!")
        return self.db

    async def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            print("Mongo Connection Closed.")

db = MongoDBClient().db
client = MongoDBClient().client