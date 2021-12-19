""""
Copyright (C) 2021 twyleg
"""
import time
import requests
import json
import logging
from typing import Dict
from winreg import *
from requests.exceptions import ReadTimeout, ConnectTimeout, ConnectionError


class Publisher:

    MICROPHONE_REGISTRY_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone\NonPackaged"
    WEBCAM_REGISTRY_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam\NonPackaged"

    class Config:
        def __init__(self):
            self.endpoint: str

        def read_config(self, filepath: str) -> None:
            config_file = open(filepath, "r")
            config_dict = json.loads(config_file.read())
            self.endpoint = config_dict['endpoint']

    def __init__(self, config: Config) -> None:
        self.config = config
        self.registry = ConnectRegistry(None, HKEY_CURRENT_USER)
        self.microphone_active = False
        self.webcam_active = False

    def get_last_used_time_stop_timestamps_from_registry(self, registry_key_str: str) -> Dict[HKEYType, any]:
        key = OpenKey(self.registry, registry_key_str)
        result = {}
        for i in range(0, QueryInfoKey(key)[0]):
            try:
                keyname = EnumKey(key, i)
                asubkey = OpenKey(key, keyname)
                val, type = QueryValueEx(asubkey, "LastUsedTimeStop")
                result[asubkey] = val
            except WindowsError:
                pass
        return result

    def is_last_used_stop_timestamp_equal_to_zero_existing(self, last_used_stop_timestamps: Dict[str, int]) -> bool:
        for last_used_stop_timestamp in last_used_stop_timestamps.values():
            if last_used_stop_timestamp == 0:
                return True
        return False

    def is_microphone_active(self) -> bool:
        last_used_time_stop_timestamps = self.get_last_used_time_stop_timestamps_from_registry(self.MICROPHONE_REGISTRY_KEY)
        return self.is_last_used_stop_timestamp_equal_to_zero_existing(last_used_time_stop_timestamps)

    def is_webcam_active(self) -> bool:
        last_used_time_stop_timestamps = self.get_last_used_time_stop_timestamps_from_registry(self.WEBCAM_REGISTRY_KEY)
        return self.is_last_used_stop_timestamp_equal_to_zero_existing(last_used_time_stop_timestamps)

    def send_state(self) -> None:
        params = {'cam': int(self.webcam_active), 'mic': int(self.microphone_active)}
        try:
            requests.get(url=self.config.endpoint, params=params, timeout=10)
            logging.info('Requested: %s', params)
        except (ReadTimeout, ConnectTimeout, ConnectionError):
            logging.error('Unable to transmit request, timeout reached')

    def update(self):
        microphone_active = self.is_microphone_active()
        webcam_active = self.is_webcam_active()

        if self.microphone_active != microphone_active or self.webcam_active != webcam_active:
            self.microphone_active = microphone_active
            self.webcam_active = webcam_active
            logging.info('State change detected: cam=%s, mic=%s', self.webcam_active, self.microphone_active)
            self.send_state()


if __name__ == '__main__':
    config = Publisher.Config()
    config.read_config('config.json')

    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
    logging.info('Started onair sign publisher with endpoint %s', config.endpoint)

    publisher = Publisher(config)
    publisher.send_state()

    while True:
        publisher.update()
        time.sleep(0.1)

