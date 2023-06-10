import sys
from datetime import date, datetime, timedelta
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# MongoDB 연결
client = MongoClient('localhost', 27017)
db = client.system_info
usage_collection = db.usage_data

# date 파라미터가 존재할 경우, 그 날짜 값을 사용하고 그렇지 않으면 현재 날짜 사용
date = sys.argv[1] if len(sys.argv) > 1 else date.today().strftime("%Y-%m-%d")

# 시작 날짜와 종료 날짜 지정
start_date = datetime.strptime(date, "%Y-%m-%d")
send_date = start_date + timedelta(days=1, seconds=-1)

# MongoDB 쿼리
results = usage_collection.find({"timestamp": {"$gte": str(start_date), "$lt": str(end_date)}})

# Threshold => 각 cpu, ram, disk에 맞는 threshold 설정 필요
threshold = 70

#plot 그리기 위한 리스트 정의
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
    time_list.append(str(time))

fig, ax = plt.subplots()

# time_list 날짜 형식을 matplotlib에서 사용하는 date 타입으로 변환
time_numbers = mdates.date2num(time_list)

ax.plot(time_numbers, cpu_list, label='CPU')
ax.plot(time_numbers, ram_list, label='RAM')
ax.plot(time_numbers, disk_list, label='Disk')

# 임계치 구간 설정하여 다르게 표시
for usage_list, color in [(cpu_list, 'blue'), (ram_list, 'green'), (disk_list, 'purple')]:
    high_usage = np.array(usage_list) > threshold
    ax.plot(time_numbers[high_usage], np.array(usage_list)[high_usage], color='red')

# x축 format 설정
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

# plot 레이아웃 구성
ax.set_xlabel('Time')
ax.set_ylabel('Usage (%)')
ax.set_title('System Usage Over Time')
ax.legend()

plt.show()
