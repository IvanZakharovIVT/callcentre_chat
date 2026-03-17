from elasticsearch import AsyncElasticsearch

from apps.core.config import settings


class ElasticsearchService:
    def __init__(self):
        self._es = AsyncElasticsearch(
            [f"http://{settings.ES_HOST}:{settings.ES_PORT}"],
        )

    async def init_index(self, index_name: str):
        if not await self._es.indices.exists(index=index_name):
            mappings = {
                "mappings": {
                    "properties": {
                        "name": {
                            "type": "text",
                            "analyzer": "russian"
                        }
                    }
                }
            }
            await self._es.indices.create(index=index_name, body=mappings)

    async def search(self, query):
        return await self._es.search(
            index='my_index',
            d={"match_all": query}
        )

    async def add_document(self, document):
        await self._es.index(index="my_index", body=document)