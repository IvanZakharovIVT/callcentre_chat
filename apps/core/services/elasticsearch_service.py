from elasticsearch import AsyncElasticsearch

from apps.core.config import settings


class ElasticsearchService:
    def __init__(self):
        self._es = AsyncElasticsearch(
            [f"http://{settings.ES_HOST}:{settings.ES_PORT}"],
        )

    async def init_index(self, index_name: str, mappings: dict):
        if not await self._es.indices.exists(index=index_name):
            await self._es.indices.create(index=index_name, body=mappings)

    async def search(self, index_name: str, query):
        return await self._es.search(
            index=index_name,
            d={"match_all": query}
        )

    async def add_document(self, index_name: str, document: dict):
        await self._es.index(index=index_name, body=document)