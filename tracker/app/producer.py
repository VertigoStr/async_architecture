from jsonschema import validate
from app.schema import schema
from aiokafka import AIOKafkaProducer
import asyncio
import json
import os


loop = asyncio.get_event_loop()
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'task')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)


async def send_notice(message: json):
    version = message['version']
    action = message['action']
    validate(instance=message, schema=schema[version][action])
    await producer.send_and_wait(
        KAFKA_TOPIC,
        json.dumps(message).encode('utf-8')
    )
