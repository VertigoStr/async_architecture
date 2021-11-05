from aiokafka import AIOKafkaProducer
import asyncio
import json
import os


loop = asyncio.get_event_loop()
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'account')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)


async def send_notice(message: json):
    await producer.send_and_wait(
        KAFKA_TOPIC,
        json.dumps(message).encode('utf-8')
    )
