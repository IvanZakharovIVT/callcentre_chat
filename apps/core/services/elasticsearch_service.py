from elasticsearch import AsyncElasticsearch

from apps.core.config import settings


class ElasticsearchService:
    def __init__(self):
        self._es = AsyncElasticsearch(
            hosts=settings.ES_SERVER,
            # basic_auth=(settings.ES_USER, settings.ES_PASSWORD)
        )

    async def search(self, query):
        return await self._es.search(
            index='my_index',
            d={"match_all": query}
        )

    async def add_document(self, document):
        await self._es.index(index="my_index", body=document)