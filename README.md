# wechatRobot
汽车博物馆聊天机器人
  
1. 在model.py 配置mysql端口号和mysql ip地址 

2. 修改robot_config.xlsx文件来配置管理员身份和机器人工作群

3.python app.py

4.依赖包安装：pip install -r requirements.txt or pip3 install -r requirements.txt

5. 运行命令 python app.py host      port user password     database or python3 app.py host port user password database
    例子： python3 app.py 127.0.0.1 3306 root ZRJ19920708 itchat
    
6.数据库新建： 1. create database itchat;
             2. CREATE TABLE CHAT_CONTENT(
                  uuid     CHAR(30),
                  WechatID CHAR(30) NOT NULL,
                  Content  TEXT,
                  Time     TIMESTAMP,
                  GroupName TEXT, 
                  GroupSize INT
                )ENGINE=innodb DEFAULT CHARSET=utf8;
