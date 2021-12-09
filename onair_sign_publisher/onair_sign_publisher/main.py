import time
import requests
import json
from typing import Dict
from winreg import *
from requests.exceptions import ReadTimeout


def check_for_missing_stop_timestamp(entry: str) -> bool:
    aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
    aKey = OpenKey(aReg, entry)
    for i in range(0, QueryInfoKey(aKey)[0]):
        try:
            keyname = EnumKey(aKey, i)
            asubkey = OpenKey(aKey, keyname)
            val, type = QueryValueEx(asubkey, "LastUsedTimeStop")
            if val == 0:
                return True
        except WindowsError:
            pass
    return False


def check_microphone_active() -> bool:
    return check_for_missing_stop_timestamp(r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone\NonPackaged")


def check_webcam_active() -> bool:
    return check_for_missing_stop_timestamp(r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam\NonPackaged")


def send_request(mic: int, cam: int) -> None:
    params = {'cam': cam, 'mic': mic}
    try:
        r = requests.get(endpoint, params=params, timeout=10)
        print(f"Requested: cam={cam}, mic={mic}")
    except ReadTimeout:
        print("Unable to transmit request, timeout reached")


def read_config(filepath: str) -> Dict:
    f = open(filepath, "r")
    return json.loads(f.read())


if __name__ == '__main__':
    oldMicState = 0
    oldCamState = 0

    config = read_config('../config.json')
    endpoint = config['endpoint']

    print(f'Started onair sign publisher with endpoint {endpoint}')

    send_request(oldMicState, oldCamState)

    while True:
        newMicState = int(check_microphone_active())
        newCamState = int(check_webcam_active())

        if oldCamState != newCamState or oldMicState != newMicState:
            print(f"State change detected: cam={newCamState}, mic={newMicState}")
            send_request(newMicState, newCamState)

            oldMicState = newMicState
            oldCamState = newCamState

        time.sleep(0.1)

