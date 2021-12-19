# Onair sign firmware

The onair sign firmware contains a small http server (based on picoweb) that accepts HTTP Get requests
with the current state of the microphone and webcam of the computer to visualize

## Prerequisites

Create a virtual environment and install requirements

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Configure WIFI

Put the desired Wifi ssid, password and http server port into _onair_sign_firmware/config.json_

## Flash software to ESP32

The _flash.py_ script will make sure that everything necessary will be transferred to your ESP32.
It will cover the following steps for you:

1. Flash a Micropython image into the ESP32
2. Copy the following files to the ESP32
   1. main.py
   2. wifi.py
   3. config.json
3. Run the _initial_setup.py_ script to install all necessary dependencies via _upip_ 

Just run the following command to execute the _flash.py_ script.

    python flash.py <SERIAL_PORT>

## Application testing

The following command will run a small toggle test script that will toggle the microphone and webcam
LEDs frequently.

    python applicationtest/toggle_test.py <IP_ADDRESS> <PORT>