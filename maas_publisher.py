import json
import psutil
import paho.mqtt.client as mqtt
import time
from pymongo import MongoClient
from datetime import datetime
import pytz

korea_tz = pytz.timezone('Asia/Seoul')
korea_time = datetime.now(korea_tz).strftime('%Y-%m-%d %H:%M:%S')

def on_connect(client, userdata, flags, rc):
    print("Connected to Mosquitto Broker")

BROKER_HOST = "localhost"
BROKER_PORT = 1883

cpu_threshold = 50
ram_threshold = 60
disk_threshold = 80

client = MongoClient('localhost', 27017)  
db = client.system_info  
usage_collection = db.usage_data 

# Connect to Mosquitto broker
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.connect(BROKER_HOST, BROKER_PORT)

# Collect and publish system info, and store it in MongoDB
while True:
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent  # '/' refers to root directory, adjust as needed

    usage_data = {
        'cpu_percent': cpu_percent,
        'ram_percent': ram_percent,
        'disk_percent': disk_percent,
        'timestamp': korea_time
    }
    
    usage_collection.insert_one(usage_data)  # store usage data in MongoDB

    # Publish data if usage is over threshold
    if cpu_percent > cpu_threshold:
        mqtt_client.publish("system_info/cpu", json.dumps({"message": "High CPU usage!", "cpu_percent": cpu_percent}))
    if ram_percent > ram_threshold:
        mqtt_client.publish("system_info/ram", json.dumps({"message": "High RAM usage!", "ram_percent": ram_percent}))
    if disk_percent > disk_threshold:
        mqtt_client.publish("system_info/disk", json.dumps({"message": "High DISK usage!", "disk_percent": disk_percent}))

    # Check system info every second
    time.sleep(1)
