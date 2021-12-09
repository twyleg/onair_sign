import picoweb
from time import sleep
from machine import Pin
from dht import DHT22
import network


if __name__ == '__main__':
    sta_if = network.WLAN(network.STA_IF)
    ipadd = sta_if.ifconfig()
    app = picoweb.WebApp(__name__)

    p0 = Pin(0, Pin.OUT)
    p1 = Pin(4, Pin.OUT)
    p0.on()
    p1.on()

    @app.route("/onair")
    def html(req, resp):
        req.parse_qs()
        cam = int(req.form['cam'])
        mic = int(req.form['mic'])
        print(f'Received: cam={cam}, mic={mic}')
        p0.value(mic)
        p1.value(cam)
        yield from picoweb.start_response(resp, status=200)

    app.run(debug=True, host=ipadd[0], port=8080)
