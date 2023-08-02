import uuid
from typing import Any
from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchema
from sqlalchemy.orm import Session

from ..utils import make_elasticsearch_query
from .definations import db, es
from .guid import GUID


class Base(db.Model):

    __abstract__ = True

    __session: Session = db.session

    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,
                    default=db.func.current_timestamp(),
                    onupdate=db.func.current_timestamp())

    def create(self):
        self.__session.add(self)
        self.__commit()

    def update(self):
        self.__commit()

    def delete(self):
        self.__session.delete(self)
        self.__commit()

    def __commit(self):
        self.__session.commit()


class ElasticSearchBase(Base):

    __abstract__ = True

    __es = es
    __schema: SQLAlchemyAutoSchema
    __schema_many: SQLAlchemyAutoSchema

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__es.options(ignore_status=[400,404]).indices.create(index=self.__tablename__)

    def create(self):
        try:
            super().create()
        except:
            raise

        doc = self.__schema.dump(self)
        self.__es.index(index=self.__tablename__, document=doc)

    def update(self, field_name, value):
        try:
            super().update()
        except:
            raise

        sq = self.__es.search(
            index=self.__tablename__,
            query={
                "match": {
                    field_name : value
                }
            }
        )

        self.__es.update(
            index = 'index_name',
            id = sq["hits"]["hits"]["_id"],
            doc = self.__schema.dump(self),
        )

    def delete(self, field_name: str, value: Any):
        try:
            super().delete()
        except:
            raise
        self.__es.delete_by_query(index=self.__tablename__, q={field_name : value})

    @classmethod
    def elasticsearch(cls, search_key: str):
        response = cls.__es.search(
            index="metadatas",
            query=make_elasticsearch_query(search_key),
        )
        data = [hit["_source"] for hit in response["hits"]["hits"]]
        return cls.__schema_many.load(data)

    @classmethod
    def set_schemas(cls, schema: SQLAlchemyAutoSchema, schema_many: SQLAlchemyAutoSchema):
        cls.__schema = schema
        cls.__schema_many = schema_many
