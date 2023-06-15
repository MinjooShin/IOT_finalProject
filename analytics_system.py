import sys
from datetime import date, datetime, timedelta
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
import numpy as np

# MongoDB 연결
client = MongoClient('172.18.147.141', 27017)
db = client.system_info

# date 파라미터와 server IP 파라미터가 존재할 경우, 그 값을 사용하고 그렇지 않으면 현재 날짜 및 'localhost'를 사용
date = sys.argv[1] if len(sys.argv) > 1 else date.today().strftime("%Y-%m-%d")
servers = sys.argv[2:] if len(sys.argv) > 2 else ['127.0.0.1']

# 시작 날짜와 종료 날짜 지정
start_date = datetime.strptime(date, "%Y-%m-%d")
end_date = start_date + timedelta(days=1, seconds=-1)

# Threshold => 각 cpu, ram, disk에 맞는 threshold 설정 필요
threshold = 70

fig, axs = plt.subplots(len(servers), squeeze=False)

# 업데이트 함수 정의
def update(num, ax, server_ip):
    ax.clear()
    usage_collection = db[str(server_ip)]
    results = usage_collection.find({"timestamp": {"$gte": str(start_date), "$lt": str(end_date)}})

    cpu_list = []
    ram_list = []
    disk_list = []
    time_list = []

    for result in results:
        # 초 단위로 날짜 형식 변환
        time = datetime.strptime(result["timestamp"], "%Y-%m-%d %H:%M:%S")
        cpu_list.append(result["cpu_percent"])
        ram_list.append(result["ram_percent"])
        disk_list.append(result["disk_percent"])
        time_list.append(time)

    time_numbers = mdates.date2num(time_list)

    ax.plot(time_numbers, cpu_list, label='CPU')
    ax.plot(time_numbers, ram_list, label='RAM')
    ax.plot(time_numbers, disk_list, label='Disk')

    for usage_list, color in [(cpu_list, 'blue'), (ram_list, 'green'), (disk_list, 'purple')]:
        high_usage = np.array(usage_list) > threshold
        ax.plot(time_numbers[high_usage], np.array(usage_list)[high_usage], color='red')

    # x축 format 설정
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    # plot 레이아웃 구성
    ax.set_xlabel('Time')
    ax.set_ylabel('Usage (%)')
    print(server_ip)
    ax.set_title(f'System Usage Over Time for server {server_ip}')
    ax.legend()

# 각 서버에 대한 동적 시각화 생성
for i, server in enumerate(servers):
    ani = animation.FuncAnimation(fig, update, fargs=(axs[i, 0], server), interval=3000, cache_frame_data=False)

plt.show()
