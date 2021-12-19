#! /usr/bin/python
""""
Copyright (C) 2021 twyleg
"""
import sys
import os
import time

global PORT


def flash_micropython(filepath: str):
    print(f'Flashing micropython: {filepath}')
    os.system(f"esptool.py --chip esp32 --port {PORT} erase_flash")
    time.sleep(1.0)
    os.system(f"esptool.py --chip esp32 --port {PORT} --baud 460800 write_flash -z 0x1000 {filepath}")
    print("Sleep for 10s while uC resets")
    time.sleep(10)


def upload(src: str, dst=''):
    print(f'Uploading: {src}')
    os.system(f'ampy --port {PORT} put {src} {dst}')


def run(filepath: str):
    print(f'Run script: {filepath}')
    os.system(f'ampy --port {PORT} run {filepath}')


def ls(path: str):
    print(f'ls: {path}')
    os.system(f'ampy --port {PORT} ls {path}')


def reset():
    print('reset')
    os.system(f'ampy --port {PORT} reset')


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('Please call the script in the following way:')
        print('\tpython flash.py <SERIAL_PORT>')
        sys.exit(-1)
    else:
        PORT = sys.argv[1]

    flash_micropython('micropython/esp32-20210902-v1.17.bin')
    upload('onair_sign_firmware/wifi.py')
    upload('onair_sign_firmware/config.json')
    upload('onair_sign_firmware/main.py')
    ls('/')
    run('onair_sign_firmware/initial_setup.py')
    reset()
