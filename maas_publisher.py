import json
import psutil
import paho.mqtt.client as mqtt
import time
from pymongo import MongoClient
from datetime import datetime
import pytz
import socket

BROKER_HOST = 'localhost'  # 브로커 호스트
BROKER_PORT = 1883  # 브로커 포트

cpu_threshold = 50
ram_threshold = 60
disk_threshold = 80

def publish_system_info(mqtt_client, ip):
    korea_tz = pytz.timezone('Asia/Seoul')
    korea_time = datetime.now(korea_tz).strftime('%Y-%m-%d %H:%M:%S')

    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent  # 루트 디렉토리 지정

    usage_data = {
        'cpu_percent': cpu_percent,
        'ram_percent': ram_percent,
        'disk_percent': disk_percent,
        'timestamp': korea_time,
        'hostname': ip
    }

    # 서버 IP를 컬렉션 이름으로 사용
    client = MongoClient('172.18.147.141', 27017)
    db = client.system_info
    usage_collection = db[str(ip)]
    usage_collection.insert_one(usage_data)

    if cpu_percent > cpu_threshold:
        mqtt_client.publish("system_info/cpu", json.dumps({"message": f"High CPU usage on {ip}!", "cpu_percent": cpu_percent}))
    if ram_percent > ram_threshold:
        mqtt_client.publish("system_info/ram", json.dumps({"message": f"High RAM usage on {ip}!", "ram_percent": ram_percent}))
    if disk_percent > disk_threshold:
        mqtt_client.publish("system_info/disk", json.dumps({"message": f"High DISK usage on {ip}!", "disk_percent": disk_percent}))

# MQTT 클라이언트 생성
mqtt_client = mqtt.Client()

# MQTT 클라이언트가 브로커에 연결
mqtt_client.connect(BROKER_HOST, BROKER_PORT)

# ip = socket.gethostbyname(socket.gethostname())
# socket.gethostbyname(socket.gethostname())를 대체
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))  # Google DNS를 사용
ip = s.getsockname()[0]
s.close()

# 3초마다 시스템 정보 확인하여, 시스템 정보를 게시하고 MongoDB에 저장
while True:
    publish_system_info(mqtt_client, ip)
    time.sleep(3)  
