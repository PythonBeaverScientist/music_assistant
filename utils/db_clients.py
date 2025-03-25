from pymongo import MongoClient

from config import settings


mongo_client = MongoClient(settings.MONGO_URI)
