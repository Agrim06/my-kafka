from confluent_kafka.admin import NewTopic
from app.client import get_admin

def create_topic():
    admin = get_admin()

    topic = NewTopic(
        topic = "rider_updates",
        num_partitions= 2,
        replication_factor= 1
    )

    futures = admin.create_topics([topic])

    for topic_name, future in futures.items():
        try:
            future.result()
            print(f"Topic created: {topic_name}")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("Topic already exists")
            else:
                print(f"Failed to create topic: {e}")

if __name__ == "__main__":
    create_topic()