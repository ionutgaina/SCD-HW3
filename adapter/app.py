import logging
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
        client.create_database(INFLUX_DB)
        return client
    except Exception as e:
        logging.error(f"Failed to connect to InfluxDB: {e}")
        sys.exit(1)


def on_message(client, userdata, message):
    pass


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
