# IOT_finalProject

## Source Python Script 실행 방법

1. Defalut Defalut (basic option)
Simple Description: Post a notification message to subscribers when a particular metric threshold is exceeded.

publisher broker: python maas_publisher.py

subscriber: python maas_subscriber.py --servers [broker_server1] [broker_server2] --ports [broker_port1] [broker_port2] --usernames None None --passwords None None

2. (추가 옵션: 현재 일자를 옵션으로 제시하는 경우, 실시간 모니터링):
python maas_publisher.py

python maas_subscriber.py --servers 172.18.147.141 192.168.0.11 --ports 1883 1883 --usernames None None --passwords None None --date 2023-06-15

한명의 구독자가 여러 서버의 시스템 정보를 tracking 하기 위한 사전 방법:
1. 각 서버에 MQTT broker 를 설치한다.
2. 각 서버에 퍼블리셔 코드를  업로드한다.
3. 각 퍼블리셔가 각자의 서버 즉, 자신의 ip 주소에 연결하기 위햇 BROKER_HOST 변수를 각 publisher의 서버 IP 주소 혹은 ‘localhost’로 설정한다.
4. 시스템 정보를 지속적으로 tracking 하기 위해서 maas_subscriber.py 스크립트 파일을 background에서 실행시켜 둔다.

각 서버에 MQTT broker 를 설치 방법 (Linux):
1. sudo apt-get update
2. sudo apt-get install mosquitto mosquitto-clients //Mosquitto 설치
3. sudo systemctl start mosquitto //Mosquitto 서비스 실행
4. sudo systemctl status mosquitto //서비스 상태 확인
5. sudo systemctl enable mosquitto //부팅시 Mosquitto 서비스 자동 시작
6. sudo ufw allow 1883 //방화벽으로 MQTT 통신 차단되지 않도록 1883 포트 열기