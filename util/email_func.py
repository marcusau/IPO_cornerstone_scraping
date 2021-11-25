#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, pathlib, sys,logging, tempfile, filetype, time

sys.path.append(os.getcwd())

parent_path = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(parent_path))

master_path = parent_path.parent
sys.path.append(str(master_path))

project_path = master_path.parent
sys.path.append(str(project_path))

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import logging
from typing import Union
from datetime import datetime

from Config.setting import config

##########################################################################################################
FORMAT = '%(levelname)s: %(asctime)-15s: %(filename)s: %(funcName)s: %(module)s: %(message)s'
logging.basicConfig(filename=config.log_file_path, level=logging.INFO, format=FORMAT)
LOGGER = logging.getLogger(__file__)

LOGGER.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler(config.log_file_path)
fileHandler.setFormatter(FORMAT)
fileHandler.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(FORMAT)
consoleHandler.setLevel(logging.DEBUG)
##########################################################################################################
# 第三方 SMTP 服务
mail_host = "smtp.hket.com"  # 设置服务器
mail_user = "marcusau@etnet.com.hk"  # 用户名
mail_pass = "iETNet001"  # 口令

sender = 'marcusau@etnet.com.hk'
receivers = ['marcusau@etnet.com.hk']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

##########################################################################################################
def send_email(credits:Union[str,int]):
    message = MIMEText(f'Remaining credits for IPO cornerstone table extraction :{str(credits)} ,please add credit and change updated API key in yaml file', 'plain', 'utf-8')
    subject = f'Remaining credit of IPO cornerstone table extraction '#{datetime.now().isoformat()


    message['From'] = Header("test", 'utf-8')
    message['To'] = Header("test", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print(f"send remaining credits to email: {' , '.join(receivers)}")
    except smtplib.SMTPException as e:
        print(f"Error: cannot send to email :{' , '.join(receivers)},  exception : {e}")

if __name__=='__main__':
    send_email(f'test')