import paho.mqtt.client as mqtt
import json
import argparse
import subprocess
from multiprocessing import Process

# Mosquitto 브로커에 연결되었을 때 실행되는 콜백 함수
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to Mosquitto Broker at {userdata['server']}:{userdata['port']}")
        client.subscribe("system_info/cpu")
        client.subscribe("system_info/ram")
        client.subscribe("system_info/disk")

        if userdata['date']:
            client.subscribe(f"system_info/analytics/{userdata['date']}")
            subprocess.Popen(["python", "analytics_system.py", userdata['date'], userdata['server']])
            
    else:
        print(f"Failed to connect, return code {rc}\n")

# Mosquitto 브로커부터 메시지를 수신받았을 때 실행되는 콜백 함수
def on_message(client, userdata, msg):
    message = json.loads(msg.payload)
    print(f'Topic: {msg.topic}, Message: {message["message"]}, Value: {message.get("cpu_percent" if "cpu" in msg.topic else "ram_percent" if "ram" in msg.topic else "disk_percent")}')

# MQTT Client 시작 함수
def start_mqtt_client(server_ip, port=1883, username=None, password=None, date=None):
    userdata = {'server': server_ip, 'port': port, 'date': date}
    mqtt_client = mqtt.Client(userdata=userdata)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    if username and password:
        mqtt_client.username_pw_set(username, password)
    try:
        mqtt_client.connect(server_ip, port)
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"Failed to connect to server {server_ip}:{port}. Error: {e}")

# commandline input 파싱
parser = argparse.ArgumentParser()
parser.add_argument("--servers", nargs='+', help="Enter the server IP addresses separated by space", required=True)
parser.add_argument("--ports", nargs='+', type=int, help="Enter the port numbers for the servers separated by space", required=True)
parser.add_argument("--usernames", nargs='+', help="Enter the username for the servers, if any. If not needed, enter 'None'", required=True)
parser.add_argument("--passwords", nargs='+', help="Enter the password for the servers, if any. If not needed, enter 'None'", required=True)
parser.add_argument("--date", help="Enter the date in format YYYY-MM-DD", default=None)
args = parser.parse_args()

# 서버 수와 포트 수와 username, password 수가 일치하는지 확인
if len(args.servers) != len(args.ports) or len(args.servers) != len(args.usernames) or len(args.servers) != len(args.passwords):
    print("Error: The number of servers, ports, usernames, and passwords must match!")
    exit(1)

# 각 서버에 대해 별도의 프로세스를 시작
if __name__ == '__main__':
    for server_ip, port, username, password in zip(args.servers, args.ports, args.usernames, args.passwords):
        Process(target=start_mqtt_client, args=(server_ip, port, username, password, args.date)).start()
