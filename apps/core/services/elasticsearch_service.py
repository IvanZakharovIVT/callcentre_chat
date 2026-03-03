from elasticsearch import Elasticsearch

from apps.core.config import settings


class ElasticsearchService:
    def __init__(self):
        self._es = Elasticsearch(hosts=settings.ES_SERVER, basic_auth=(settings.ES_USER, settings.ES_PASSWORD))
