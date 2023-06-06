import json

import psutil
import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected to Mosquitto Broker")


BROKER_HOST = "localhost"
BROKER_PORT = 1883

cpu_threshold = 80
ram_threshold = 90

# Mosquitto 브로커에 연결
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.connect(BROKER_HOST, BROKER_PORT)

# 시스템 정보를 주기적으로 발행
while True:
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent

    # Mosquitto 브로커에 데이터 발행
    if cpu_percent > cpu_threshold:
        mqtt_client.publish("system_info", json.dumps({"message": "High CPU usage!", "cpu_percent": cpu_percent}))
    if ram_percent > ram_threshold:
        mqtt_client.publish("system_info", json.dumps({{"message": "High RAM usage!", "ram_percent": ram_percent}}))

    # 1초마다 주기적으로 시스템 정보 확인
    time.sleep(1)
