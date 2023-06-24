import os

from elasticsearch import Elasticsearch
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
es = Elasticsearch(
    "https://elasticsearch.localhost:9200/",
    http_auth=(os.environ.get("ELASTICSEARCH_USERNAME"),os.environ.get("ELASTICSEARCH_PASSWORD")),
    verify_certs=False
)
