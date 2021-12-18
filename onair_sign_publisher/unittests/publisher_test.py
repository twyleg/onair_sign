import unittest
import sys
import requests
import fake_winreg
sys.modules['winreg'] = fake_winreg
import onair_sign_publisher.publisher as publisher
from unittest.mock import MagicMock


MICROPHONE_REGISTRY_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone\NonPackaged\TestApplication"
WEBCAM_REGISTRY_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam\NonPackaged\TestApplication"

class PublisherTest(unittest.TestCase):

    def setUp(self) -> None:
        fake_registry = fake_winreg.fake_reg_tools.get_minimal_windows_testregistry()
        fake_winreg.load_fake_registry(fake_registry)
        reg_handle = fake_winreg.ConnectRegistry(None, fake_winreg.HKEY_CURRENT_USER)
        self.cam_key_handle = fake_winreg.CreateKeyEx(reg_handle, WEBCAM_REGISTRY_KEY, 0, fake_winreg.KEY_WRITE)
        self.mic_key_handle = fake_winreg.CreateKeyEx(reg_handle, MICROPHONE_REGISTRY_KEY, 0, fake_winreg.KEY_WRITE)

        self.config = publisher.Publisher.Config()
        self.config.endpoint = 'http://localhost:8080/onair_sign'
        self.publisher = publisher.Publisher(self.config)

        requests.get = MagicMock()

    def set_mic_active(self, is_active: bool) -> None:
        fake_winreg.SetValueEx(self.mic_key_handle, 'LastUsedTimeStop', 0, fake_winreg.REG_DWORD, int(not is_active))

    def set_cam_active(self, is_active: bool) -> None:
        fake_winreg.SetValueEx(self.cam_key_handle, 'LastUsedTimeStop', 0, fake_winreg.REG_DWORD, int(not is_active))

    def expect_no_state_update(self):
        requests.get.assert_not_called()

    def expect_state_update(self, mic_state: bool, cam_state: bool):
        expected_params = {'cam': int(cam_state), 'mic': int(mic_state)}
        requests.get.assert_called_with(url=self.config.endpoint, params=expected_params, timeout=10)

    def expect_state_update_once(self, mic_state: bool, cam_state: bool):
        expected_params = {'cam': int(cam_state), 'mic': int(mic_state)}
        requests.get.assert_called_once_with(url=self.config.endpoint, params=expected_params, timeout=10)

    def test__mic_active__is_mic_active__return_active(self):
        self.set_mic_active(True)
        self.assertEqual(True, self.publisher.is_microphone_active(), 'incorrect microphone state')

    def test__cam_active__is_cam_active__return_active(self):
        self.set_cam_active(True)
        self.assertEqual(True, self.publisher.is_webcam_active(), 'incorrect webcam state')

    def test__mic_inactive__is_mic_inactive__return_inactive(self):
        self.set_mic_active(False)
        self.assertEqual(False, self.publisher.is_microphone_active(), 'incorrect microphone state')

    def test__cam_inactive__is_cam_inactive__return_inactive(self):
        self.set_cam_active(False)
        self.assertEqual(False, self.publisher.is_webcam_active(), 'incorrect webcam state')

    def test__cam_and_mic_inactive__no_changes__no_update_sent(self):
        self.set_cam_active(False)
        self.set_mic_active(False)
        self.publisher.update()
        self.publisher.update()
        self.expect_no_state_update()

    def test__cam_and_mic_active__no_changes__no_update_sent(self):
        self.set_cam_active(True)
        self.set_mic_active(True)
        self.publisher.update()
        self.publisher.update()
        self.publisher.update()
        self.expect_state_update_once(mic_state=True, cam_state=True)

    def test__cam_inactive__cam_becomes_active__update_sent(self):
        self.set_cam_active(True)
        self.set_mic_active(False)
        self.publisher.update()
        self.expect_state_update(mic_state=False, cam_state=True)

    def test__mic_inactive__mic_becomes_active__update_sent(self):
        self.set_cam_active(False)
        self.set_mic_active(True)
        self.publisher.update()
        self.expect_state_update(mic_state=True, cam_state=False)

    def test__mic_and_cam_inactive__mic_and_cam_toggled__updates_sent(self):
        self.set_cam_active(False)
        self.set_mic_active(True)
        self.publisher.update()
        self.expect_state_update(mic_state=True, cam_state=False)

        self.set_cam_active(True)
        self.set_mic_active(False)
        self.publisher.update()
        self.expect_state_update(mic_state=False, cam_state=True)

        self.set_cam_active(True)
        self.set_mic_active(True)
        self.publisher.update()
        self.expect_state_update(mic_state=True, cam_state=True)

        self.set_cam_active(False)
        self.set_mic_active(False)
        self.publisher.update()
        self.expect_state_update(mic_state=False, cam_state=False)


