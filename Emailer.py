#!/usr/local/bin/python3

import os
import socks
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

sender = "lixiangyujiayou@gmail.com"
password = "fPMd4VR2tL2JA9jnsVe8"
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1086)
# socks.wrapmodule(smtplib)

def mail(receivers=[], subject='Test', content='Test email', image_path=''):
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1086)
    socks.wrapmodule(smtplib)

    message = MIMEMultipart()

    message['From'] = Header("From 数据分析", 'utf-8')  # 发送者
    message['To'] = Header("需求方", 'utf-8')  # 接收者
    message['Subject'] = Header(subject, 'utf-8')

    text = MIMEText(content, 'plain', 'utf-8')
    message.attach(text)

    image_data = open(image_path, 'rb').read()
    image = MIMEImage(image_data, name=os.path.basename(image_path))
    message.attach(image)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender, password)
        server.sendmail(sender, receivers, message.as_string())
        server.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


class Emailer:
    sender = "lixiangyujiayou@gmail.com"
    password = "fPMd4VR2tL2JA9jnsVe8"
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    def __init__(self, config):
        sender = config['(地址)']
        if sender is None or len(sender) == 0:
            raise RuntimeError('未找到sender')

        password = config['(密码)']
        if password is None or len(password) == 0:
            raise RuntimeError('未找到password')

        smtp_server = config['(服务器)']
        if smtp_server is None or len(smtp_server) == 0:
            raise RuntimeError('未找到smtp server')

        smtp_port = config['(端口号)']
        if smtp_port == 0:
            raise RuntimeError('未找到smtp port')

        self.sender = sender
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1086)
        socks.wrapmodule(smtplib)

    def run(self, input_results={}, email={}):
        receivers = email['(收件箱)']
        if receivers is None or len(receivers) is 0:
            raise RuntimeError('未找到收件箱')

        title = email['(标题)']
        if receivers is None or len(receivers) is 0:
            raise RuntimeError('未找到标题')

        FROM = email['(FROM)']
        if FROM is None or len(FROM) is 0:
            FROM = self.sender

        TO = email['(TO)']
        if TO is None or len(TO) is 0:
            TO = ','.join(receivers)

        contents = email['(内容)']
        if contents is None or len(contents) is 0:
            raise RuntimeError('未找到内容')

        message = MIMEMultipart()

        message['From'] = Header(FROM, 'utf-8')  # 发送者
        message['To'] = Header(TO, 'utf-8')  # 接收者
        message['Subject'] = Header(title, 'utf-8')

        for content in contents:
            if content.count('(TODAY)'):
                content = content.replace('(TODAY)', time.strftime('%Y-%m-%d', time.localtime()))

            if content in input_results.keys():
                path = input_results[content]

                if os.path.splitext(path)[-1] == '.jpg':
                    image_data = open(path, 'rb').read()
                    image = MIMEImage(image_data, name=content)
                    message.attach(image)
            else:
                text = MIMEText(content, 'plain', 'utf-8')
                message.attach(text)

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, receivers, message.as_string())
        server.quit()
