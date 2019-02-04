#!/usr/local/bin/python3

import requests
import time
import hashlib
import hmac
import Utils


def get_auth(secret: str, project: str, ai: str, tm: str):
    message = ("POST\n/auth/token\nproject=" + project + "&ai=" + ai + "&tm=" + tm).encode('utf-8')
    signature = hmac.new(bytes(secret.encode('utf-8')), bytes(message), digestmod=hashlib.sha256).hexdigest()
    print('auth is ' + signature)
    return signature


def get_token():
    timestamp = int(time.time() * 1000 + 60 * 1000)
    print('timestamp is ' + str(timestamp))

    auth = get_auth('cd7074a4d06b47e58dfff6fd2068cb2e', '1P6j1bVP', 'a5006f6a0d3a6aab', str(timestamp))
    headers = {'X-Client-Id': '408caa8f3a8c47f298e64d8da6df24ae'}
    params = {'ai': 'a5006f6a0d3a6aab', 'project': '1P6j1bVP', 'tm': str(timestamp), 'auth': auth}
    url = 'https://www.growingio.com/auth/token'
    response = requests.post(url, headers=headers, data=params)
    print('response is ' + response.text)

    token = response.json()['code']
    print('token is ' + token)

    return token


def get_headers():
    token = get_token()
    headers = {'Authorization': token, 'X-Client-Id': '408caa8f3a8c47f298e64d8da6df24ae'}
    return headers


def get_params(days: int = 7, interval: int = 86400000):
    params = {'startTime': Utils.day_before_today_begin_timestamp(days),
              'endTime': Utils.yesterday_end_timestamp(),
              'interval': interval}
    print(params)
    return params


def get_dashboard(project: str = '1P6j1bVP', dashboard: str = 'GR4jBQao'):
    headers = get_headers()
    url = 'https://www.growingio.com/projects/%s/dashboards/%s.json' % (project, dashboard)
    response = requests.get(url, headers=headers)
    print('dashboard %s is %s' % (dashboard, response.text))
    return response.json()


def get_chart(project: str = '1P6j1bVP', chart: str = 'noqL2nAP', days: int = 7, interval: int = 86400000):
    headers = get_headers()
    params = get_params(days, interval)
    url = 'https://www.growingio.com/v2/projects/%s/charts/%s.json' % (project, chart)
    response = requests.get(url, headers=headers, params=params)
    print('chart %s is %s' % (chart, response.text))
    return response.json()

