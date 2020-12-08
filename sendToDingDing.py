#!/usr/bin/env python3
#coding=utf-8

import os
import datetime
import yaml
import json
import urllib.request
from apscheduler.schedulers.blocking import BlockingScheduler
from tianqi import  get_data,getHTMLText

pid = os.getpid()
f = open('/root/py/DingDing_pid','w')
print(pid,file=f)
f.close()

conf_file = '/root/py/config.yml'
config = open(conf_file)
conf = yaml.load(config,Loader=yaml.FullLoader)
config.close()

test_webhook = conf.get('webhook').get('test')
url = conf.get('tianqi').get('url')
days = conf.get('tianqi').get('days')
html = getHTMLText(url)
tianqi_list = get_data(html)

umbrella_png = "![screenshot](http://8.129.59.238:80/umbrella.png)"
hot_png = "![screenshot](http://8.129.59.238:80/hot.png)"
cold_png = "![screenshot](http://8.129.59.238:80/cold.png)"
pingpong_png = "![screenshot](http://8.129.59.238:80/pingpong.png)"

print("==========table============")
print(tianqi_list[0][1])
def morning_message(tianqi_list):
    message = "早上好晴崽崽！\n\n今天天气%s，最高温度%s度，最低温度%s度，风力%s。\n\n"%(tianqi_list[0][1],tianqi_list[0][2],tianqi_list[0][3],tianqi_list[0][4])
    if "雨" in tianqi_list[0][1] or "雪" in tianqi_list[0][1]:
        message = message + "今天有雨，可别忘记带伞哦~" + umbrella_png
    elif int(tianqi_list[0][2]) > 30:
        message = message + "今天很热哦，可以穿凉爽一些。" + hot_png
    elif int(tianqi_list[0][3]) < 15:
        message = message + "今天有点冷，一定要穿外套呀！" + cold_png
    else:
        message = message + "今天温度真舒适，要不要约个球？" + pingpong_png
    return message


def evening_message(tianqi_list):
    message = "晚上好晴崽崽！\n\n明天天气%s，最高温度%s度，最低温度%s度，风力%s。\n\n"%(tianqi_list[1][1],tianqi_list[1][2],tianqi_list[1][3],tianqi_list[1][4])
    if "雨" in tianqi_list[1][1] or "雪" in tianqi_list[0][1]:
        message = message + "明天有雨，可别忘记带伞哦~" + umbrella_png
    elif int(tianqi_list[1][2]) > 30:
        message = message + "明天很热哦，可以穿凉爽一些。" + hot_png
    elif int(tianqi_list[1][3]) < 15:
        message = message + "明天有点冷，一定要穿外套呀！" + cold_png
    else:
        message = message + "明天温度真舒适，要不要约个球？" + pingpong_png
    return message


print(tianqi_list[0][2])
try:
    morning_messages = morning_message(tianqi_list)
except:
    pass
noon_messages = conf.get('messages').get('noon')[0]
evening_messages = evening_message(tianqi_list)

print(morning_messages)
print(evening_messages)

def sendToDingDing(webhook,message):
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    my_data = {
        "msgtype": "markdown",
        "markdown": {"title": "温馨提示",
                      "text": message
                     },
        "at": {

            "isAtAll": True
        }
    }
    sendData = json.dumps(my_data)  # 将字典类型数据转化为json格式
    sendDatas = sendData.encode("utf-8")  # python3的Request要求data为byte类型
    request = urllib.request.Request(url=webhook, data=sendDatas, headers=header)
    # 将请求发回的数据构建成为文件格式
    opener = urllib.request.urlopen(request)
    # 打印返回的结果
    print(opener.read())

#通过定时任务执行早中晚三次发送消息的任务
scheduler = BlockingScheduler(daemonic = False)

#(year=None, month=None, day=None, week=None, day_of_week=None, hour=None, minute=None, second=None, start_date=None, end_date=None, timezone=None)
@scheduler.scheduled_job('cron', day_of_week='0-6', hour='8', minute='30', second='*/20')
def send_message_job():
    sendToDingDing(test_webhook,morning_messages)

@scheduler.scheduled_job('cron', day_of_week='0-6', hour='12', minute='5', second='20')
def send_message_job():
    sendToDingDing(test_webhook,noon_messages)

@scheduler.scheduled_job('cron', day_of_week='0-6', hour='18', minute='20', second='*/20')
def send_message_job():
    sendToDingDing(test_webhook,evening_messages)


scheduler.start()
