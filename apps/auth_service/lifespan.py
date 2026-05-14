import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.auth_service.cunsumer import KafkaConsumer
from apps.core.config import settings
from apps.core.database import AsyncSession, engine
from apps.auth_service.auth.services.user_service import UserService

logger = logging.getLogger(__name__)

# Глобальный объект консьюмера
kafka_consumer = KafkaConsumer(settings.BOOTSTRAP_SERVER)

# Kafka topics for user status events
USER_STATUS_TOPICS = ["user-connected", "user-disconnected", "user-activity"]

async def handle_message(message: dict, topic: str, partition: int, offset: int):
    logger.info(f"Received message from {topic}:")
    logger.info(f"  Message: {message}")
    logger.info(f"  Partition: {partition}, Offset: {offset}")

    # Process message based on topic
    event_type = message.get("event_type")
    user_uuid = message.get("user_uuid")
    
    if not user_uuid:
        logger.error(f"Missing user_uuid in message: {message}")
        return

    # Create a database session for this message
    async with AsyncSession() as session:
        user_service = UserService(session)
        
        try:
            if topic == "user-connected" or event_type == "user_connected":
                await user_service.handle_user_connected(user_uuid)
                logger.info(f"User {user_uuid} marked as online")
                
            elif topic == "user-disconnected" or event_type == "user_disconnected":
                await user_service.handle_user_disconnected(user_uuid)
                logger.info(f"User {user_uuid} marked as offline")
                
            elif topic == "user-activity" or event_type == "user_activity":
                await user_service.handle_user_activity(user_uuid)
                logger.info(f"User {user_uuid} activity updated")
                
            else:
                logger.warning(f"Unknown topic or event type: {topic}, {event_type}")
                
        except Exception as e:
            logger.error(f"Error processing message for user {user_uuid}: {e}")
            await session.rollback()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await kafka_consumer.start(
        topics=USER_STATUS_TOPICS,
        message_handler=handle_message
    )
    logger.info(f"Kafka consumer started for topics: {USER_STATUS_TOPICS}")
    yield
    # Shutdown
    await kafka_consumer.stop()
    logger.info("Kafka consumer stopped")
