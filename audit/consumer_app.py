import json
import os
import asyncio
from jsonschema import validate
from app.schema import schema
from aiokafka import AIOKafkaConsumer
from app.models.database import database
from app.utils import users as users_utils
from app.utils import tasks as tasks_utils


KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'task')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

loop = asyncio.get_event_loop()


async def update_user(data: dict):
    await users_utils.update_user(data)


async def create_user(data: dict):
    await users_utils.create_user(data)


async def make_user_inactive(data: dict):
    await users_utils.make_user_inactive(data)


async def set_task_price(data: dict):
    await tasks_utils.set_task_price(data['task_id'])


async def task_assigned(data: dict):
    await tasks_utils.set_task_assigned(data['task_id'], data['user_id'])


async def task_completed(data: dict):
    await tasks_utils.set_task_completed(data['task_id'], data['user_id'])


ACTION_MAP = {
    'user_updated': update_user,
    'user_created': create_user,
    'user_inactive': make_user_inactive,
    'task_created': set_task_price,
    'task_assigned': task_assigned,
    'task_completed': task_completed,
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
            version = message['version']
            action = message['action']
            validate(instance=message, schema=schema[version][action])
            await ACTION_MAP[message['action']](message['data'])
    finally:
        await consumer.stop()
        await database.disconnect()


loop.run_until_complete(consume())
