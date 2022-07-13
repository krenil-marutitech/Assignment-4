import config
from elasticsearch import Elasticsearch, helpers
import warnings

warnings.filterwarnings(action='ignore')


IndexName = config.INDEX_NAME
ESHost = config.ES_HOST


es = Elasticsearch(hosts=[ESHost])


class ESKNN():

    def __init__(self):
        pass

    def create_index(self):
        body = {}

        try:
            result = es.indices.create(index=IndexName, body=body, ignore=400)

            if 'error' in result:
                return 2
            else:
                return 1
        except:
            return 0

    def insert_user(self, data):
        rows = []

        for item in data:
            rows.append({
                '_index': IndexName,
                '_source': item
            })

        result = helpers.bulk(es, rows, request_timeout=30)

        return result

    def fetch_messages(self, query, field_name):
        result = es.search(
            request_timeout=30,
            index=IndexName,
            body={
                "query": {
                    "bool": {
                        "must": [
                            {
                                "wildcard": {
                                    field_name: {
                                        "value": "*" + query + "*"
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        )

        return result

    def fetch_messages_by_time(self, query):
        try:
            result = es.search(
                request_timeout=30,
                index=IndexName,
                body={
                    'query': {
                        'match': {
                            'created_time': {
                                'query': query
                            }
                        }
                    }
                }
            )
            return result
        except:
            return 0

    def get_all_users(self):
        result = es.search(
            request_timeout=30,
            index=IndexName,
            size=100,
            body={
                'query': {
                    'match_all': {}
                }
            }
        )

        return result