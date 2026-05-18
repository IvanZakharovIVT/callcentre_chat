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
kafka_producer = KafkaProducer(settings.BOOTSTRAP_SERVER)

async def init_elasticsearch_index():
    service = ElasticsearchService()
    mappings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "russian_english_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "russian_stemmer", "english_stemmer"]
                    }
                },
                "filter": {
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "russian_english_analyzer"
                },
                "username": {
                    "type": "text",
                },
                "email": {
                    "type": "text",
                },
                "chat_id": {
                    "type": "integer",
                },
                "message_id": {
                    "type": "integer",
                },
                "timestamp": {
                    "type": "date",
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

