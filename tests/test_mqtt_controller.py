from unittest import TestCase, mock
from jsonschema import ValidationError
from mqttrdc.mqtt_controller import MQTTController
import json


class FakeMQTTMessage:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")


class TestHandleMessage(TestCase):
    def setUp(self) -> None:
        self.controller = MQTTController()

    @mock.patch(
        "mqttrdc.mqtt_controller.MQTTController.volume",
        new_callable=mock.PropertyMock,
    )
    def test_volume_commands(self, mock_volume):
        mock_volume.return_value = None

        # test all valid volume values
        for volume in range(101):
            cmd = FakeMQTTMessage({"volume": volume})
            self.controller.handle_message(cmd)
            mock_volume.assert_called_once()
            mock_volume.reset_mock()

        # test not valid volume values
        for volume in (-1, 101, "10", 50.5):
            cmd = FakeMQTTMessage({"volume": volume})
            self.assertRaises(ValidationError, self.controller.handle_message, cmd)

    @mock.patch("mqttrdc.mqtt_controller.MQTTController.volume_up")
    @mock.patch("mqttrdc.mqtt_controller.MQTTController.volume_down")
    def test_volume_ctrl_commands(self, mock_volume_down, mock_volume_up):
        mock_volume_up.return_value = None
        mock_volume_down.return_value = None

        # test volume up command
        cmd = FakeMQTTMessage({"volumeCtrl": "+"})
        self.controller.handle_message(cmd)
        mock_volume_up.assert_called_once()

        # test volume down command
        cmd = FakeMQTTMessage({"volumeCtrl": "-"})
        self.controller.handle_message(cmd)
        mock_volume_down.assert_called_once()

        # test not valid volume ctrl values
        for volume_ctrl in ("++", "--", "+-", "-+"):
            cmd = FakeMQTTMessage({"volumeCtrl": volume_ctrl})
            self.assertRaises(ValidationError, self.controller.handle_message, cmd)

    @mock.patch(
        "mqttrdc.mqtt_controller.MQTTController.mute",
        new_callable=mock.PropertyMock,
    )
    def test_mute_commands(self, mock_mute):
        mock_mute.return_value = None

        # test all valid mute values
        for mute in (True, False):
            cmd = FakeMQTTMessage({"mute": mute})
            self.controller.handle_message(cmd)
            mock_mute.assert_called_once()
            mock_mute.reset_mock()

        # test not valid volume values
        for mute in (1, 0, "true", "True", "false", "False"):
            cmd = FakeMQTTMessage({"mute": mute})
            self.assertRaises(ValidationError, self.controller.handle_message, cmd)

    @mock.patch("mqttrdc.mqtt_controller.MQTTController.toggle_mute")
    @mock.patch("mqttrdc.mqtt_controller.MQTTController.toggle_pause")
    def test_toggle_commands(self, mock_toggle_pause, mock_toggle_mute):
        mock_toggle_mute.return_value = None
        mock_toggle_pause.return_value = None

        # test toggle mute command
        cmd = FakeMQTTMessage({"toggle": "mute"})
        self.controller.handle_message(cmd)
        mock_toggle_mute.assert_called_once()

        # test toggle pause command
        cmd = FakeMQTTMessage({"toggle": "pause"})
        self.controller.handle_message(cmd)
        mock_toggle_pause.assert_called_once()

        # test not valid toggle values
        for toggle in ("Mute", "Pause", "play", "Play", 1, 0):
            cmd = FakeMQTTMessage({"toggle": toggle})
            self.assertRaises(ValidationError, self.controller.handle_message, cmd)

    def test_invalid_command(self):
        cmd = FakeMQTTMessage({"msg": "This is an invalid command"})
        self.assertRaises(ValueError, self.controller.handle_message, cmd)
