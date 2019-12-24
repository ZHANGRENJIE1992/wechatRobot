# -*- coding: utf-8 -*-
import itchat
from itchat.content import *
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import shutil
import pandas as pd
import threading
import _thread
import datetime
from model import db
from common import Excel
from data import *
import sys
import os,time
from convert import convert 

#record log
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'w')
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass

# User message monitoring
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend_msg(msg):
    df = pd.read_excel('robot_config.xlsx', sheet_name='Config')
    print("handle_friend_msg")
    # Send command and Get response from FileHelper
    try:
        if msg['User']['NickName'] in list(df['Robot name']):
            if msg['Type'] == TEXT:
                itchat.send("Robot received admin message.", toUserName=msg['FromUserName'])
                print("Robot received your message." + msg['User']['NickName'])
                if "request" in msg['Content']:
                    itchat.send_file('robot_config.xlsx', toUserName=msg['FromUserName'])
                    print("Robot sent your file." + msg['User']['NickName'])
            if msg['Type'] == ATTACHMENT and msg['FileName'] == "robot_config.xlsx":
                msg.download(msg['FileName'])
                itchat.send("Robot received your config file.", toUserName=msg['FromUserName'])
                print("Robot received your file." + msg['User']['NickName'])
    except Exception as e:
        print(e)
    # msg_id = msg['MsgId']
    # msg_from_user = msg['User']['NickName']
    # msg_content = msg['Content']
    # msg_create_time = msg['CreateTime']
    # msg_type = msg['Type']


# Group message monitoring
@itchat.msg_register([TEXT], isGroupChat=True)
def handle_group_msg(msg):
    target_group = []
    try:
        df = pd.read_excel('robot_config.xlsx', sheet_name='Target Groups')
    except Exception as e:
        print(e)
    for group_name in list(df['Target Groups']):
        chat_rooms = itchat.search_chatrooms(name=group_name)
        if(chat_rooms):
            target_group.append(chat_rooms[0]['UserName'])
    if msg['FromUserName'] in target_group:
        #print(msg)
        if(msg['Type']=='Text'):
           sql =db(keyinfo)
           now = datetime.datetime.now()
           now_str = now.strftime("%Y-%m-%dT%H:%M:%S")
           sql.create_data(wechatid=str(msg['ActualNickName']),content=str(msg['Content']),time=str(now_str),groupid=str(msg['User']['NickName']),groupsize=str(msg['User']['MemberCount']))
        if msg.isAt:  # Check if robot is @
            df = pd.read_excel('robot_config.xlsx', sheet_name='QA')
            question = list(df['Q'])
            answer = list(df['A'])
            df = pd.read_excel('robot_config.xlsx', sheet_name='Config')
            robot_name = df['Robot name'][0]
            msg_q = msg['Text'].replace("@" + robot_name + "\u2005", "", 1).strip()
            print("aaa:",msg_q)
            if msg_q == "":
                answerguide = "请使用@小助手 + 以下关键字:'参观时间','闭馆时间','门票','门票优惠','团队购票','免票','讲解','地址','怎么去博物馆','电话','发票',来获取相关信息"
                itchat.send_msg(answerguide,toUserName=msg['FromUserName'])
            if msg_q in question:
                itchat.send_msg(answer[question.index(msg_q)],
                                toUserName=msg['FromUserName'])

    # group  = itchat.get_chatrooms(update=True)
    # from_user = ''
    # for g in group:
    #     if g['NickName'] == '全时履约一体化':#从群中找到指定的群聊
    #         from_group = g['UserName']
    #         for menb in g['MemberList']:
    #             #print(menb['NickName'])
    #             if menb['NickName'] == "履约助手":#从群成员列表找到用户,只转发他的消息
    #                 from_user = menb['UserName']
    #                 break
    #     if g['NickName'] == '一只小鸟飞':#把消息发到这个群
    #         to_group = g['UserName']
    # if msg['FromUserName'] == from_group:
    #     if msg['ActualUserName'] == from_user:
    #         itchat.send('%s:%s'%(msg['ActualNickName'],msg['Content']),to_group)

def send_sched_msg():
    target_group = []
    name = generate_dailydata()
    df = pd.read_excel('robot_config.xlsx', sheet_name='Target Groups')
    df_admin = pd.read_excel('robot_config.xlsx', sheet_name='Config') #找出config表中的admin
    name = generate_dailydata()
    AdminUserName_group=[]
    for admins in list(df_admin['Robot name']):
        user = itchat.search_friends(admins)
        itchat.send_file(name, toUserName=user[0]['UserName'])

    for group_name in list(df['Target Groups']):
        chat_rooms = itchat.search_chatrooms(name=group_name)
        if(chat_rooms):
            target_group.append(chat_rooms[0]['UserName'])
    for g in target_group:
        itchat.send_msg(str(df['Scheduler Content'][0]),
                        toUserName=g)



def scheduler_msg():
    while True:
        df = pd.read_excel('robot_config.xlsx', sheet_name='Scheduler')
        # print(df)
        time.sleep(60)
        now = datetime.datetime.now()
        now_str = now.strftime('%Y/%m/%d %H:%M')[11:]
        set_time = str(df['Time'][0])
        print(now_str)
        print(set_time)
        if now_str == set_time:
            send_sched_msg()


# Show login success message
def after_login():
    itchat.send_msg("Robot is Activated.", toUserName="filehelper")
    itchat.send_msg("You can use the following command:", toUserName="filehelper")
    itchat.send_msg("a: xxx\nb: xxx\nc: xxx", toUserName="filehelper")
    # sched.add_job(save_data, 'cron', hour=23, minute=58, second=0)
    # sched.add_job(send_data, 'cron', hour=23, minute=59, second=0)
    # sched.start()


# Show logout message
def after_logout():
    itchat.send_msg("Robot logout, please re-login.", toUserName="filehelper")
    # sched.shutdown()


# Configure Robot by Excel settings
# def robot_config():
#     df = pd.read_excel('robot_config.xlsx', sheet_name='Config')


def save_data():
    current_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    data.to_excel(current_date + '.xlsx', sheet_name='data2', index = False)
    itchat.send_msg("Data saved.", toUserName="filehelper")


def send_data():
    current_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    itchat.send_file(current_date + '.xlsx', toUserName="filehelper")
    itchat.send_msg("Data sent.", toUserName="filehelper")

def generate_dailydata():
    now = datetime.datetime.now()#提取年月日
    now_str = now.strftime('%Y-%m-%d')
    #export_dataset=[]  #导出所有数据 
    #export_data = {} #单个群数据字典 {"sheet_name": groupname,"data":meta_data}
    #metaData = []#单个数据字典中的数据 一共6个不同时间段的数组 
    #timeData = []#单个数据时间段的数组 "日期","时间段","群昵称","群人数","新增人数","活跃数","活跃账号","关键词参观时间出现次数","关键词闭馆时间出现次数","关键词门票出现次数","关键词门票优惠出现次数","关键词团队购票出现次数","关键词免票出现次数","关键词讲解出现次数","关键词地址出现次数","关键词怎么去博物馆出现次数","关键词电话出现次数","关键词发票出现次数"
    sql=db(keyinfo)
    rawdata = sql.get_dailyinfo(now.year,now.month,now.day)
    #print(rawdata)
    groupname = handle_rawdata_groupname(rawdata)
    #print(groupname)

    export_dataset = groupchatcontentbygroupname(groupname,rawdata)

    obj = {}
    obj["title"]= ["日期","时间段","群昵称","群人数","活跃数","活跃账号","关键词参观时间出现次数","关键词闭馆时间出现次数","关键词门票出现次数","关键词门票优惠出现次数","关键词团队购票出现次数","关键词免票出现次数","关键词讲解出现次数","关键词地址出现次数","关键词怎么去博物馆出现次数","关键词电话出现次数","关键词发票出现次数"]
    fix = "daily.xls"
    name = f"{now_str}_{fix}"
    excel = Excel()
    wb = excel.createExcel(obj["title"], export_dataset,name)
    return name

def main(argv):
    global keyinfo
    keyinfo = convert(argv)
    data = {}
    sched = BlockingScheduler()
    # Auto re-login
    try:
        itchat.auto_login(hotReload=True, loginCallback=after_login, exitCallback=after_logout)
    except Exception:

    time.sleep(5)  # 5 sec for ready

    # t1 = threading.Thread(target=itchat.run(), args=())
    # t2 = threading.Thread(target=scheduler_msg, args=())
    # t1.start()
    # t2.start()
    _thread.start_new_thread(scheduler_msg, ())
    _thread.start_new_thread(itchat.run(), ())


if __name__ == '__main__':
    # Initialize the robot
    
    main(sys.argv)
    
    

