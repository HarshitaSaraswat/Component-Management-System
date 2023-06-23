import json

from elasticsearch import Elasticsearch

from ..metadatas.models import Metadata
from ..metadatas.schemas import metadata_schema

ELASTIC_PASSWORD = "bmUkFmqEahjDzmg47JkN"

es = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", ELASTIC_PASSWORD),
    verify_certs=False
)

q = Metadata.query.filter(Metadata.id=="90d484e41704428db63c146a447c84c8").one_or_none()

doc = metadata_schema.dump(q)
print("doc = ", doc)

# resp = es.index(index="test-index", document=doc)
# print("result = ",resp['result'])


query = {
                "more_like_this" : {
                    "fields" : ["name"],
                    "like" : "zaxis_coupling_5x8mm",
                    "min_term_freq" : 1,
                    "max_query_terms" : 12
                }
            }

query2 = {
    "fuzzy" : {
        # "fields" : ["name"],
        "name": {
                "value": "zaxis coupling",
                "fuzziness":"AUTO",
                "transpositions":True,
                "max_expansions": 100,
                "boost": 5
            }
    }
}

r = es.search(
    index="test-index",
    query=query2,
)
print(json.dumps(dict(r), indent=4))
