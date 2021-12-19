""""
Copyright (C) 2021 twyleg
"""
import wifi
import upip

print('Started install_dependencies.py')

ssid, psk = wifi.read_connection_details_from_file()
wifi.connect(ssid, psk)

upip.install([
    'picoweb',
    'micropython-ulogging'
], 'lib/')
