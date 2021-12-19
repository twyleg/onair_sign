""""
Copyright (C) 2021 twyleg
"""
import picoweb
import network
import wifi
import json
from machine import Pin

if __name__ == '__main__':

    print('Read config from flash')
    with open('config.json', 'r') as config_file:
        data = config_file.read()
        config = json.loads(data)
        http_port = config['http_port']

    print('Setting up WIFI connection')
    ssid, psk = wifi.read_connection_details_from_file()
    wifi.connect(ssid, psk)

    print('Starting picoweb server')
    sta_if = network.WLAN(network.STA_IF)
    ipadd = sta_if.ifconfig()
    app = picoweb.WebApp(__name__)

    print('Initialising ports')
    p0 = Pin(0, Pin.OUT)
    p1 = Pin(4, Pin.OUT)
    p0.off()
    p1.off()

    @app.route("/onair")
    def html(req, resp):
        req.parse_qs()
        cam = int(req.form['cam'])
        mic = int(req.form['mic'])
        print(f'Received: cam={cam}, mic={mic}')
        p0.value(mic)
        p1.value(cam)
        yield from picoweb.start_response(resp, status=200)

    app.run(debug=True, host=ipadd[0], port=http_port)
