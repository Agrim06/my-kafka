import sys
import json

from app.client import get_consumer

def start_consumer(group_id):
    consumer = get_consumer(group_id)

    consumer.subscribe(["rider-updates"])

    print(f"Consumer started: {group_id}")
    print("\n")

    try:
        while True:

            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Consumer error:", msg.error())
                continue

            data = json.loads(msg.value().decode("utf-8"))

            print(
                f"{group_id}: "
                f"[{msg.topic()}] "
                f"PART:{msg.partition()} "
                f"OFFSET:{msg.offset()} "
                f"DATA:{data}"
            )

    except KeyboardInterrupt:
        print("Stopping consumer...")

    finally:
        consumer.close()


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python -m app.consumer <group_id>")
        sys.exit(1)

    group_id = sys.argv[1]

    start_consumer(group_id)
