import time
import sys
import logging
import fake_winreg
sys.modules['winreg'] = fake_winreg
import onair_sign_publisher.publisher as publisher


MICROPHONE_REGISTRY_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone\NonPackaged\TestApplication"
WEBCAM_REGISTRY_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam\NonPackaged\TestApplication"


class PublisherApplicationTest:

    def __init__(self) -> None:
        logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)

        fake_registry = fake_winreg.fake_reg_tools.get_minimal_windows_testregistry()
        fake_winreg.load_fake_registry(fake_registry)
        reg_handle = fake_winreg.ConnectRegistry(None, fake_winreg.HKEY_CURRENT_USER)
        self.cam_key_handle = fake_winreg.CreateKeyEx(reg_handle, WEBCAM_REGISTRY_KEY, 0, fake_winreg.KEY_WRITE)
        self.mic_key_handle = fake_winreg.CreateKeyEx(reg_handle, MICROPHONE_REGISTRY_KEY, 0, fake_winreg.KEY_WRITE)

        self.config = publisher.Publisher.Config()
        self.config.read_config('config.json')
        self.publisher = publisher.Publisher(self.config)

    def set_mic_active(self, is_active: bool) -> None:
        fake_winreg.SetValueEx(self.mic_key_handle, 'LastUsedTimeStop', 0, fake_winreg.REG_DWORD, int(not is_active))

    def set_cam_active(self, is_active: bool) -> None:
        fake_winreg.SetValueEx(self.cam_key_handle, 'LastUsedTimeStop', 0, fake_winreg.REG_DWORD, int(not is_active))

    def run(self) -> None:
        while True:
            self.set_cam_active(False)
            self.set_mic_active(True)
            self.publisher.update()
            time.sleep(1.0)

            self.set_cam_active(True)
            self.set_mic_active(False)
            self.publisher.update()
            time.sleep(1.0)

            self.set_cam_active(True)
            self.set_mic_active(True)
            self.publisher.update()
            time.sleep(1.0)

            self.set_cam_active(False)
            self.set_mic_active(False)
            self.publisher.update()
            time.sleep(1.0)


if __name__ == '__main__':
    publisher_application_test = PublisherApplicationTest()
    publisher_application_test.run()