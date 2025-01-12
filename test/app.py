import logging
from json import dumps
from random import choice, uniform
from time import sleep

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
TOPIC_PREFIX = "UPB/"
BATTERY_RANGE = range(1, 101)
TEMPERATURE_RANGE = range(15, 101)
HUMIDITY_RANGE = range(10, 76)
DELAY_MIN = 0.1
DELAY_MAX = 2.0
STATIONS = ["STATION_1", "STATION_2", "STATION_3"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def create_mqtt_connection(broker_host):
    client = mqtt.Client()
    client.connect(broker_host)
    client.loop_start()
    return client


def close_mqtt_connection(client):
    client.loop_stop()
    client.disconnect()


def generate_iot_data():
    return {
        "BAT": choice(BATTERY_RANGE),
        "TMP": choice(TEMPERATURE_RANGE),
        "HUMID": choice(HUMIDITY_RANGE),
    }


def publish_data(client, topic_prefix, stations):
    station = choice(stations)
    iot_data = generate_iot_data()
    topic = f"{topic_prefix}{station}"

    client.publish(topic, dumps(iot_data))
    logging.info(f"Published to {topic}:\n{dumps(iot_data, indent=4)}")


def main():
    client = create_mqtt_connection(BROKER_HOST)

    try:
        while True:
            publish_data(client, TOPIC_PREFIX, STATIONS)
            sleep(uniform(DELAY_MIN, DELAY_MAX))
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully...")
    finally:
        close_mqtt_connection(client)


if __name__ == "__main__":
    main()
