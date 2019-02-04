#!/usr/local/bin/python3

import os
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

    emails = []  # 邮件
    inputs = {}  # 数据

    def __init__(self, config: dict, emails: list, inputs: dict):
        if config is None:
            raise RuntimeError('未找到邮箱配置')

        if inputs is None or len(inputs) == 0:
            raise RuntimeError('未找到上下文数据')

        if emails is None or len(emails) == 0:
            raise RuntimeError('未找到邮件配置')

        sender = config['(地址)']
        if len(sender) == 0:
            raise RuntimeError('未找到邮箱地址')

        password = config['(密码)']
        if len(password) == 0:
            raise RuntimeError('未找到邮箱密码')

        smtp_server = config['(服务器)']
        if len(smtp_server) == 0:
            raise RuntimeError('未找到邮箱服务器')

        smtp_port = config['(端口号)']
        if smtp_port == 0:
            raise RuntimeError('未找到邮箱端口号')

        self.inputs = inputs
        self.emails = emails

        self.sender = sender
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1086)
        socks.wrapmodule(smtplib)

    def run(self):
        for email in self.emails:
            self.operate(email)

    # inputs格式 {文件名: 路径}
    def operate(self, email):
        # (邮件):
        #   - (收件箱):
        #     - 'lixiangyujiayou@gmail.com'
        #     - 'huan.cao@bitmax.io'
        #     (标题): '(TODAY) 交易数据'
        #     (FROM): '曹欢'
        #     (TO): '需求方'
        #     (内容):
        #       - '交易数据表'
        #       - '交易-2019-01-07.jpg'
        #       - '交易-2019-01-07.xls'
        #       - '这是总结'

        receivers = email['(收件箱)']
        if len(receivers) is 0:
            raise RuntimeError('收件箱长度0')

        title = email['(标题)']
        if len(title) is 0:
            raise RuntimeError('标题长度0')

        title = Keywords.active_date(title)

        if '(FROM)' in email.keys():
            FROM = email['(FROM)']
            if len(FROM) is 0:
                FROM = self.sender
        else:
            FROM = self.sender

        if '(TO)' in email.keys():
            TO = email['(TO)']
            if len(TO) is 0:
                TO = ', '.join(receivers)
        else:
            TO = ', '.join(receivers)

        contents = email['(内容)']
        if len(contents) is 0:
            raise RuntimeError('内容长度0')

        message = MIMEMultipart()
        message['From'] = Header(FROM, 'utf-8')  # 发送者
        message['To'] = Header(TO, 'utf-8')  # 接收者
        message['Subject'] = Header(title, 'utf-8')

        # html = '<html><body><table>'
        for content in contents:
            content = Keywords.active_date(content)
            if content in self.inputs.keys():
                path = self.inputs[content]
                file_ext = os.path.splitext(path)[-1]
                if file_ext == '.jpg' or file_ext == '.png':
                    image_data = open(path, 'rb').read()

                    # html += '<tr><td>'
                    # img_base64 = str(base64.b64encode(image_data), encoding="utf-8")
                    # html += '<img src="data:image/png;base64,' + img_base64 + '" width="720" height="360"/>'
                    # html += '</td></tr>'

                    # html += '<tr><td><img src="https://assets.growingio.com/webapp1/img-13iYfFi.png"></td></tr>'

                    image = MIMEImage(image_data, name=content)
                    message.attach(image)
            else:
                if content[-1] != '\n':
                    content += '\n'

                # html += '<tr><td><h2>'
                # html += content
                # html += '</h2></td></tr>'

                content = '<h2>' + content + '</h2>'
                text = MIMEText(_text=content, _subtype='html', _charset='utf-8')
                message.attach(text)

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
