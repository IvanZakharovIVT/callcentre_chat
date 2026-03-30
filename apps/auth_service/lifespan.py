import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.auth_service.cunsumer import KafkaConsumer

logger = logging.getLogger(__name__)

# Глобальный объект консьюмера
kafka_consumer = KafkaConsumer()

async def handle_message(message: dict, topic: str, partition: int, offset: int):
    logger.info(f"Received message from {topic}:")
    logger.info(f"  Message ID: {message.get('message_id')}")
    logger.info(f"  Data: {message.get('data')}")
    logger.info(f"  Source: {message.get('source')}")
    logger.info(f"  Partition: {partition}, Offset: {offset}")

    # Здесь ваша бизнес-логика обработки сообщения
    # Например, сохранение в БД, вызов внешних API и т.д.

    # Имитация обработки
    await process_message(message)

async def process_message(message: dict):
    # Ваша логика обработки
    logger.info(f"Processing message: {message.get('message_id')}")
    # TODO: Добавить реальную обработку
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await kafka_consumer.start(
        topics=["default-topic", "another-topic"],
        message_handler=handle_message
    )
    logger.info("Kafka consumer started")
    yield
    # Shutdown
    await kafka_consumer.stop()
    logger.info("Kafka consumer stopped")
