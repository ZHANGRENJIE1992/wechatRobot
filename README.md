# wechatRobot

# 汽车博物馆聊天机器人

### 1. 修改robot_config.xlsx文件来配置管理员身份和机器人工作群

### 2. pip install -r requirements.txt or pip3 install -r requirements.txt

### 3. python app.py host port user password database or python3 app.py host port user password database

### e.g. python3 app.py 127.0.0.1 3306 root ZRJ19920708 itchat

### 4. database init
~~~~sql 
    CREATE DATABASE itchat;
    
    CREATE TABLE CHAT_CONTENT(
      uuid     CHAR(30),
      WechatID CHAR(30) NOT NULL,
      Content  TEXT,
      Time     TIMESTAMP,
      GroupName TEXT, 
      GroupSize INT
    )ENGINE=innodb DEFAULT CHARSET=utf8;
~~~~
