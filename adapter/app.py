from datetime import datetime
import json
import logging
import re
import sys
import os
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
INFLUX_HOST = "influxdb"
INFLUX_DB = "iot_data"
BROKER_HOST = "mqtt"
TOPIC = "#"

DB_CLIENT = None
MQTT_CLIENT = None


def setup_logging(debug: bool):
    log_level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=log_level,
    )


def setup_influxdb():
    try:
        client = InfluxDBClient(host=INFLUX_HOST, database=INFLUX_DB)
        existing_dbs = client.get_list_database()
        if not any(db["name"] == INFLUX_DB for db in existing_dbs):
            client.create_database(INFLUX_DB)
        return client
    except Exception as e:
        logging.error(f"Failed to connect to InfluxDB: {e}")
        sys.exit(1)


def save_data(location: str, station: str, data: dict):
    if "timestamp" not in data:
        timestamp = datetime.now().strftime(DATE_FORMAT)
        logging.debug(f"Using current time as timestamp: {timestamp}")
    else:
        timestamp = datetime.strptime(data["timestamp"], DATE_FORMAT)
        logging.debug(f"Using provided timestamp: {timestamp}")

    bd_data = []

    for key, value in data.items():
        if not isinstance(value, (int, float)):
            continue

        bd_data.append(
            {
                "measurement": f"{location}.{station}.{key}",
                "tags": {"location": location, "station": station},
                "fields": {"value": float(value)},
                "time": timestamp,
            }
        )

        logging.debug(f"Saving data: {bd_data}")

    DB_CLIENT.write_points(bd_data)


def on_message(client, userdata, message):
    if not re.match(r"^[\w-]+/[\w-]+$", message.topic):
        logging.debug(f"Invalid topic: {message.topic}")
        return

    logging.debug(f"Received message on topic {message.topic}")

    location, station = message.topic.split("/")

    try:
        payload = json.loads(message.payload)
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON payload: {message.payload}")
        return

    try:
        save_data(location, station, payload)
    except Exception as e:
        logging.error(f"Failed to save data: {e}")


def setup_mqtt():
    try:
        client = mqtt.Client()
        client.on_message = on_message
        client.connect(BROKER_HOST)
        client.subscribe(TOPIC)
        return client
    except Exception as e:
        logging.error(f"Failed to connect to MQTT broker: {e}")
        sys.exit(1)


if __name__ == "__main__":
    debug_mode = os.getenv("DEBUG_DATA_FLOW", "false").lower() == "true"
    setup_logging(debug_mode)
    try:
        DB_CLIENT = setup_influxdb()
        MQTT_CLIENT = setup_mqtt()
        MQTT_CLIENT.loop_forever()
    except KeyboardInterrupt:
        logging.info("Exiting gracefully")
        sys.exit(0)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
