from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient

BOOTSTRAP_SERVERS = "localhost:9092"

def get_admin():
    return AdminClient({
        "bootstrap.servers" : BOOTSTRAP_SERVERS
    })

def get_producer():
    return Producer({
        "bootstrap.servers" : BOOTSTRAP_SERVERS,
        "client.id" : "my-app"
    })

def get_consumer(group_id):
    return Consumer({
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True
    })