from aiokafka import AIOKafkaConsumer
import json
import asyncio
from typing import Callable


class KafkaConsumer:
    def __init__(self, bootstrap_servers: str = "localhost:9092", group_id: str = "app2-group"):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        self.message_handler = None

    async def start(self, topics: list, message_handler: Callable):
        self.message_handler = message_handler
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        await self.consumer.start()

        # Запускаем фоновую задачу для обработки сообщений
        asyncio.create_task(self.consume())

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume(self):
        try:
            async for msg in self.consumer:
                if self.message_handler:
                    await self.message_handler(msg.value, msg.topic, msg.partition, msg.offset)
        except Exception as e:
            print(f"Error in consumer: {e}")
