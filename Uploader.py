#!/usr/local/bin/python3

import requests

def upload(image: bytes):
    response = requests.post(url, headers=headers, data=params)

