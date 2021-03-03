# -*- coding:utf-8 -*-
#!/usr/bin/env python
# Author: JISO
# Email: 747142549@qq.com
# File: sendEmail.py


import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import os
from email import encoders
from email.mime.base import MIMEBase


def send_mail(error_message, subject, recipients, file_paths=None):
    """
    发送邮件方法
    :param error_message: 文本信息
    :param subject: 邮件主题
    :param recipients: 收件人,即使是只发给一个人也要传list类型
    :param file_paths: 附件路径,如果有附件,需要以数组包裹字符串的形式传输["文件路径"]
    :return:
    """
    host = "******"  # 地址
    port = 25  # 端口
    user = "****"  # 用户名
    pwd = "****"  # 密码
    sender = "*****"  # 发件人

    message = MIMEMultipart()
    message["From"] = sender  # 发件人
    message["To"] = ",".join(recipients)  # 收件人
    message["Subject"] = Header(subject, "utf-8")  # 主题

    if file_paths and isinstance(file_paths, list):  # 如果附件并且类型为数组类型
        for file_path in file_paths:
            file_path_list = file_path.split(os.sep)
            file_name = file_path_list.pop()

            # 添加附件信息
            with open(file_path, "rb") as file:
                file_msg = MIMEBase("application", "octet-stream")
                file_msg.set_payload(file.read())
                file.close()

            encoders.encode_base64(file_msg)
            basename = os.path.basename(file_name)
            file_msg.add_header("Content-Disposition", "attachment", filename=("gbk", "", basename))
            message.attach(file_msg)

    # 添加文本信息
    text_msg = MIMEText(error_message)
    message.attach(text_msg)

    smtp = smtplib.SMTP()
    smtp.connect(host, port)
    smtp.login(user, pwd)
    smtp.sendmail(sender, recipients, message.as_string())  # 发送
    smtp.quit()
