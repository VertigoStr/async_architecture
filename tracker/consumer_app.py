import json
import os
import asyncio
from aiokafka import AIOKafkaConsumer
from app.models.database import database
from app.utils import users as users_utils


KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'account')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

loop = asyncio.get_event_loop()


async def update_user(data: dict):
    await users_utils.update_user(data)


async def create_user(data: dict):
    await users_utils.create_user(data)


async def make_user_inactive(data: dict):
    await users_utils.make_user_inactive(data)


ACTION_MAP = {
    'user_updated': update_user,
    'user_created': create_user,
    'user_inactive': make_user_inactive,
}


async def consume():
    await database.connect()
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        loop=loop,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value.decode())
            await ACTION_MAP[message['action']](message['data'])
    finally:
        await consumer.stop()
        await database.disconnect()


loop.run_until_complete(consume())
