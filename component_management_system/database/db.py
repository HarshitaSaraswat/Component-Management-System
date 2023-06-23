import uuid

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .guid import GUID

db = SQLAlchemy()
ma = Marshmallow()

es_engine = create_engine("elasticsearch:///?Server=127.0.0.1&Port=9200&User=admin&Password=123456")

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
    __es_session = sessionmaker(bind=es_engine)()

    def create(self):
        try:
            super().create()
        except:
            raise

        self.__es_session.add(self)
        self.__commit()

    def update(self):
        try:
            super().update()
        except:
            raise
        self.__commit()

    def delete(self):
        try:
            super().delete()
        except:
            raise
        self.__es_session.delete(self)
        self.__commit()

    def __commit(self):
        return self.__es_session.commit()
