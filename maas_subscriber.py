import paho.mqtt.client as mqtt
import json

# Mosquitto 브로커에 연결되었을 때 실행되는 콜백 함수
def on_connect(client, userdata, flags, rc):
    print("Connected to Mosquitto Broker")
    client.subscribe("system_info")

# Mosquitto 브로커부터 메시지를 수신받았을 때 실행되는 콜백 함수
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    data = json.loads(message)

    message = data["message"]
    print(message)

    # 시스템 정보 추출
    if message == "High CPU usage!":
        cpu_percent = data["cpu_percent"]
        print("value : " + cpu_percent)
    elif message == "High RAM usage!":
        ram_percent = data["ram_percent"]
        print("value : " + ram_percent)

# Mosquitto 브로커에 연결
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)

# Mosquitto 브로커로부터 메시지를 지속적으로 처리하기 위해 루프 실행
mqtt_client.loop_forever()
