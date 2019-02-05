#!/usr/local/bin/python3

import os
import platform
import socks
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import Keywords
# import base64


class Emailer:
    sender = ''
    password = ''
    smtp_server = ''
    smtp_port = 0

    email = {}  # 邮件
    inputs = {}  # 数据

    # inputs格式 {文件名: 路径}
    def __init__(self, mailbox: dict, email: dict, inputs: dict):
        if mailbox is None:
            raise RuntimeError('未找到邮箱')

        if email is None:
            raise RuntimeError('未找到邮件配置')

        if inputs is None:
            raise RuntimeError('未找到上下文数据')

        sender = mailbox['(地址)']
        if len(sender) == 0:
            raise RuntimeError('未找到邮箱地址')

        password = mailbox['(密码)']
        if len(password) == 0:
            raise RuntimeError('未找到邮箱密码')

        smtp_server = mailbox['(服务器)']
        if len(smtp_server) == 0:
            raise RuntimeError('未找到邮箱服务器')

        smtp_port = mailbox['(端口号)']
        if smtp_port == 0:
            raise RuntimeError('未找到邮箱端口号')

        self.email = email
        self.inputs = inputs

        self.sender = sender
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        sysstr = platform.system()
        if sysstr == "Windows":
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1080)
            socks.wrapmodule(smtplib)
        else:
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1086)
            socks.wrapmodule(smtplib)


    def run(self):
        receivers = self.email['(收件箱)']
        if len(receivers) is 0:
            raise RuntimeError('收件箱长度0')

        title = self.email['(标题)']
        if len(title) is 0:
            raise RuntimeError('标题长度0')

        title = Keywords.active_date(title)

        if '(FROM)' in self.email.keys():
            FROM = self.email['(FROM)']
            if len(FROM) is 0:
                FROM = self.sender
        else:
            FROM = self.sender

        if '(TO)' in self.email.keys():
            TO = self.email['(TO)']
            if len(TO) is 0:
                TO = ', '.join(receivers)
        else:
            TO = ', '.join(receivers)

        contents: list = self.email['(内容)']
        if len(contents) == 0:
            raise RuntimeError('内容长度0')

        message = MIMEMultipart()
        message['From'] = Header(FROM, 'utf-8')  # 发送者
        message['To'] = Header(TO, 'utf-8')  # 接收者
        message['Subject'] = Header(title, 'utf-8')

        # html = '<html><body><table>'
        for content in contents:
            # (类型): (文本)  # (文本)、(图片)
            # (字号): (H1)
            # (输入): '全部用户页面浏览量趋势图'
            content_type = content['(类型)']
            if content_type == '(文本)':
                font_size = content['(字号)']

            input_key = content['(输入)']
            input_key = Keywords.active_date(input_key)

            if content_type == '(文本)':
                if input_key[-1] != '\n':
                    input_key += '\n'

                # html += '<tr><td><h2>'
                # html += content
                # html += '</h2></td></tr>'

                content = '<%s>%s</%s>' % (font_size, input_key, font_size)
                text = MIMEText(_text=content, _subtype='html', _charset='utf-8')
                message.attach(text)
            else:
                if input_key not in self.inputs.keys():
                    raise RuntimeError('未找到 %s 路径' % input_key)

                path = self.inputs[input_key]
                if content_type == '(图片)':
                    image_data = open(path, 'rb').read()

                    # html += '<tr><td>'
                    # img_base64 = str(base64.b64encode(image_data), encoding="utf-8")
                    # html += '<img src="data:image/png;base64,' + img_base64 + '" width="720" height="360"/>'
                    # html += '</td></tr>'

                    # html += '<tr><td><img src="https://assets.growingio.com/webapp1/img-13iYfFi.png"></td></tr>'

                    image = MIMEImage(image_data, name=input_key)
                    message.attach(image)

        # html += '</table></body></html>'
        # text = MIMEText(_text=html, _subtype='html', _charset='utf-8')
        # message.attach(text)

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, receivers, message.as_string())
        server.quit()
