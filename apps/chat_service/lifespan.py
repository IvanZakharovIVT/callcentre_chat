from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.core.config import settings
from apps.core.services.elasticsearch_service import ElasticsearchService


@asynccontextmanager
async def lifespan(app: FastAPI):
    service = ElasticsearchService()
    await service.init_index(settings.ES_INDEX)
    yield
