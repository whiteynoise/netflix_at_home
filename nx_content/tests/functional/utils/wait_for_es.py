from elasticsearch import Elasticsearch
from functional.settings import ES_CONFIG
from functional.utils.waiter import get_waiter

if __name__ == "__main__":
    es_client = Elasticsearch(
        hosts="{host}:{port}".format(**ES_CONFIG),
        verify_certs=False,
    )
    get_waiter(es_client, 20)
