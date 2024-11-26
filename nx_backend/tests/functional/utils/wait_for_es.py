import time

from elasticsearch import Elasticsearch

from functional.settings import ES_CONFIG


if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts='{host}:{port}'.format(**ES_CONFIG),
        verify_certs=False,
    )

    while True:
        if es_client.ping():
            break
        time.sleep(20)
