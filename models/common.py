from abc import ABC
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Any

from bson import ObjectId
from pymongo import MongoClient

from config import settings


class MongoDatabaseIsEmpty(Exception):
    pass


def is_database_has_collections(client: MongoClient, database: str) -> bool:
    return bool(client[database].list_collection_names())


@dataclass
class Field:
    type_: type
    value: Any
    is_primary_key: bool = False

    def validate(self):
        if not isinstance(self.value, self.type_):
            raise TypeError(f'{self.type_} is expected for field, got {type(self.value)}')


@dataclass
class UserSettings:
    language_code: str
    is_bot: bool
    is_premium: bool

    @property
    def value(self) -> dict:
       return asdict(self)


class BaseMongoModel(ABC):

    DATABASE = settings.MONGO_INITDB_DATABASE

    @classmethod
    @property
    def COLLECTION(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def __init__(self, *args, **kwargs):
        self.created_at = Field(datetime, datetime.now())
        self.validate()

    def validate(self) -> None:
        [field.validate() for _, field in vars(self).items()]

    def __repr__(self):
        return f"{self.__class__.__name__}: {vars(self)}"

    def post(self, client: MongoClient) -> str:
        return client[self.DATABASE][self.COLLECTION].insert_one(vars(self)).inserted_id

    def post_unique(self, client: MongoClient) -> str:
        for name, field in vars(self).items():
            if field.is_primary_key and (obj_ := self.get(client, {name: field.value})):
                return obj_.get('_id')
        return client[self.DATABASE][self.COLLECTION].insert_one(vars(self)).inserted_id

    def get_by_id(self, client: MongoClient, _id: str) -> dict:
        if not is_database_has_collections(client, self.DATABASE):
            raise MongoDatabaseIsEmpty(f"mongodb database: {self.DATABASE} is empty")
        return client[self.DATABASE][self.COLLECTION].find_one({'_id': ObjectId(_id)})

    def get(self, client: MongoClient, value_with_name: dict[str, str]) -> dict:
        if not is_database_has_collections(client, self.DATABASE):
            raise MongoDatabaseIsEmpty(f"mongodb database: {self.DATABASE} is empty")
        return client[self.DATABASE][self.COLLECTION].find_one(value_with_name)
