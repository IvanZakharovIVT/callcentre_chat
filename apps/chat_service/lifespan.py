from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from apps.chat_service.producer import KafkaProducer
from apps.core.config import settings
from apps.core.services.elasticsearch_service import ElasticsearchService


class Message(BaseModel):
    data: dict
    topic: str = "default-topic"

# Глобальный объект продюсера
kafka_producer = KafkaProducer()

async def init_elasticsearch_index():
    service = ElasticsearchService()
    mappings = {
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "russian"
                },
                "username": {
                    "type": "text",
                },
                "email": {
                    "type": "text",
                },
            }
        }
    }
    await service.init_index(settings.ES_INDEX, mappings)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_elasticsearch_index()
    await kafka_producer.start()
    print("Kafka producer started")
    yield
    await kafka_producer.stop()
    print("Kafka producer stopped")

