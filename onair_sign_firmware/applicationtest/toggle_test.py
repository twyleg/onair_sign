#! /usr/bin/python
""""
Copyright (C) 2021 twyleg
"""
import sys
import time
import requests


def send_state(endpoint: str, cam_state: bool, mic_state: bool) -> None:
    params = {'cam': int(cam_state), 'mic': int(mic_state)}
    requests.get(url=endpoint, params=params, timeout=3)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Please call the script in the following way:')
        print('\tpython toggle_test.py <IP> <PORT>')
        sys.exit(-1)

    address = sys.argv[1]
    port = sys.argv[2]

    url = f'http://{address}:{port}/onair'

    while True:
        send_state(url, cam_state=False, mic_state=True)
        time.sleep(1.0)
        send_state(url, cam_state=True, mic_state=False)
        time.sleep(1.0)
        send_state(url, cam_state=True, mic_state=True)
        time.sleep(1.0)
        send_state(url, cam_state=False, mic_state=False)
        time.sleep(1.0)
