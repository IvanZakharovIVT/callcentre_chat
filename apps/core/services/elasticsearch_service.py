from elasticsearch import AsyncElasticsearch

from apps.core.config import settings
from apps.core.services.kibana_service import KibanaService


class ElasticsearchService:
    def __init__(self):
        self._es = AsyncElasticsearch(
            [f"http://{settings.ES_HOST}:{settings.ES_PORT}"],
        )
        self._kibana = KibanaService()

    async def init_index(self, index_name: str, mappings: dict):
        if not await self._es.indices.exists(index=index_name):
            await self._es.indices.create(index=index_name, body=mappings)
            await self._kibana.create_data_view(index_name, time_field="timestamp")

    async def search(self, index_name: str, query: str):
        return await self._es.search(
            index=index_name,
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["content", "username"]
                    }
                }
            }
        )

    async def add_document(self, index_name: str, document: dict):
        await self._es.index(index=index_name, body=document)