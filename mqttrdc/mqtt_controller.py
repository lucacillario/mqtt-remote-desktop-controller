"""MQTT Remote Desktop Controller.

This module lets the user to remotely control some multimedia functionalities of his
desktop/laptop, using the MQTT protocol.

Two MQTT topics:

1. `MQTT_CONTROL_TOPIC`: used to receive commands from the user.
    Commands are expected to be in JSON format.

2. `MQTT_STATUS_TOPIC`: used to notify the user of status updates (volume/mute).
    Status updates are sent in JSON format.

Examples
--------
Below is the list of supported commands, in JSON format:

Sets the volume to 100%:
>>> {"volume": 100}

Increases and decreases the volume by `VOLUME_STEP`:
>>> {"volumeCtrl": "+"}
>>> {"volumeCtrl": "-"}

Mute and unmute:
>>> {"mute": true}
>>> {"mute": false}

Toggle mute/unmute and play/pause:
>>> {"toggle": "mute"}
>>> {"toggle": "pause"}
"""

from json import JSONDecodeError
from alsaaudio import ALSAAudioError

# to run the unittest in an environment without an audio device
try:
    from alsaaudio import Mixer
except ALSAAudioError as e:
    if __name__ == "__main__":
        raise
    else:
        print(f"No audio device: {e}")
        Mixer = None

import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties

# to run the unittest in an environment without a display Server
try:
    from pynput.keyboard import Key, Controller as KeyboardController
except ImportError as e:
    if __name__ == "__main__":
        raise
    else:
        print(f"Cannot import pynput: {e}")
        Key = None
        KeyboardController = None

import json
from jsonschema import validate, ValidationError
import logging
import sys
import time
from typing import Any
from mqttrdc.mqtt_controller_manager import MQTTControllerManager


class MQTTController:
    """A class used to remote control some desktop functionalities over MQTT protocol.

    Attributes
    ----------
    volume_schema: dict
        JSON Schema of volume commands
    volume_ctrl_schema: dict
        JSON Schema of volume ctrl commands
    mute_schema: dict
        JSON Schema of mute commands
    toggle_schema: dict
        JSON Schema of toggle commands
    audio_mixer: `alsaaudio.Mixer`
        Used to control desktop volume
    keyboard: `pynput.keyboard.Controller`
        Used to simulate keyboard actions
    mqttc: `paho.mqtt.client.Client`
        MQTT client
    config: `MQTTControllerManager`
        Configuration manager, used to configure instances of this class
    """

    volume_schema = {
        "type": "object",
        "properties": {"volume": {"type": "integer", "minimum": 0, "maximum": 100}},
    }

    volume_ctrl_schema = {
        "type": "object",
        "properties": {"volumeCtrl": {"type": "string", "enum": ["+", "-"]}},
    }

    mute_schema = {
        "type": "object",
        "properties": {"mute": {"type": "boolean"}},
    }

    toggle_schema = {
        "type": "object",
        "properties": {"toggle": {"type": "string", "enum": ["mute", "pause"]}},
    }

    def __init__(self):
        self.audio_mixer = Mixer() if Mixer else None
        self.keyboard = KeyboardController() if KeyboardController else None
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_message = self.on_message
        self.mqttc.on_disconnect = self.on_disconnect
        self.config = MQTTControllerManager()

    def on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        flags: dict,
        rc: int,
        properties: Properties = None,
    ) -> None:
        """Defines the `on_connect` callback implementation.

        See `paho.mqtt.client.Client.on_connect` for more information.
        """
        if rc == 0:
            logging.info(
                f"Successfully connected to the broker {self.config.broker}: flags={flags}, properties={properties}"
            )
        else:
            logging.error(
                f"Cannot connect to the broker {self.config.broker}: error code={rc}"
            )

    @staticmethod
    def on_publish(client: mqtt.Client, userdata: Any, mid: int) -> None:
        """Defines the `on_publish` callback implementation.

        See `paho.mqtt.client.Client.on_publish` for more information.
        """
        logging.info(f"Successfully published a message: mid={mid}")

    @staticmethod
    def on_subscribe(
        client: mqtt.Client,
        userdata: Any,
        mid: int,
        granted_qos: int,
        properties: Properties = None,
    ) -> None:
        """Defines the `on_subscribe` callback implementation.

        See `paho.mqtt.client.Client.on_subscribe` for more information.
        """
        logging.info(
            f"Successfully subscribed to topic: mid={mid}, granted qos={granted_qos}, properties={properties}"
        )

    def handle_message(self, msg: mqtt.MQTTMessage) -> None:
        """Processes the received message and performs the corresponding action.

        Parameters
        ----------
        msg: `paho.mqtt.client.MQTTMessage`
            The received message to process

        Raises
        ------
        UnicodeDecodeError
            if message decoding fails
        JSONDecodeError
            if message JSON decoding fails
        ValidationError
            if message JSON Schema validation fails
        ValueError
            if message contains an invalid command
        """
        payload = json.loads(msg.payload.decode("utf-8"))
        logging.info(f"Received a new message: {payload}")
        if "volume" in payload:
            validate(payload, schema=self.volume_schema)
            self.volume = payload["volume"]
        elif "volumeCtrl" in payload:
            validate(payload, schema=self.volume_ctrl_schema)
            self.volume_up() if payload["volumeCtrl"] == "+" else self.volume_down()
        elif "mute" in payload:
            validate(payload, schema=self.mute_schema)
            self.mute = payload["mute"]
        elif "toggle" in payload:
            validate(payload, schema=self.toggle_schema)
            self.toggle_mute() if payload["toggle"] == "mute" else self.toggle_pause()
        else:
            raise ValueError(f"Cannot handle message: {payload}, not a valid command")

    def on_message(
        self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage
    ) -> None:
        """Defines the `on_message` callback implementation.

        See `paho.mqtt.client.Client.on_message` for more information.
        """
        try:
            self.handle_message(msg)
        except UnicodeDecodeError as e:
            logging.error(f"Cannot decode message: {msg.payload}, {e}")
        except JSONDecodeError:
            logging.error(
                f"Cannot deserialize message: {msg.payload.decode('utf-8')}, not a valid JSON"
            )
        except ValidationError as e:
            logging.error(f"Invalid JSON Schema: {e.message}")
        except ValueError as e:
            logging.error(str(e))
        except Exception as e:
            logging.error(f"Unexpected error while receiving a new message: {e}")

    def on_disconnect(self, client: mqtt.Client, userdata: Any, rc: int) -> None:
        """Defines the `on_disconnect` callback implementation.

        See `paho.mqtt.client.Client.on_disconnect` for more information.
        """
        if rc == mqtt.MQTT_ERR_SUCCESS:
            logging.info(
                f"Successfully disconnected from the broker {self.config.broker}"
            )
            sys.exit(0)
        else:
            logging.critical(
                f"Unexpected disconnection from the broker {self.config.broker}: error code={rc}"
            )
            sys.exit(1)

    @property
    def volume(self) -> int:
        """Gets the current volume.

        Returns
        -------
        int
            current volume integer percentage
        """
        return self.audio_mixer.getvolume()[0]

    @volume.setter
    def volume(self, value: int) -> None:
        """Sets the volume.

        Parameters
        ----------
        value: int
            volume integer percentage
        """
        self.audio_mixer.setvolume(value)
        self.update_status()

    def volume_up(self) -> None:
        """Increases the volume.

        The volume is increased by `VOLUME_STEP`, given in the configurations file.
        """
        self.volume = min(self.volume + self.config.volume_step, 100)

    def volume_down(self) -> None:
        """Decreases the volume.

        The volume is decreased by `VOLUME_STEP`, given in the configurations file.
        """
        self.volume = max(self.volume - self.config.volume_step, 0)

    @property
    def mute(self) -> bool:
        """Gets the mute status.

        Returns
        -------
        bool
            True if mute, False otherwise
        """
        return bool(self.audio_mixer.getmute()[0])

    @mute.setter
    def mute(self, value: bool) -> None:
        """Sets the mute status.

        Parameters
        ----------
        value: bool
            updated mute status
        """
        self.audio_mixer.setmute(value)
        self.update_status()

    def toggle_mute(self) -> None:
        """Toggle mute status."""
        self.mute = not self.mute

    def toggle_pause(self) -> None:
        """Toggle play/pause status by simulating a space bar press."""
        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)

    @property
    def status(self) -> dict:
        """Gets the current status.

        Returns
        -------
        dict
            a dictionary containing the current volume/mute status

        Notes
        -----
        `play/pause` status is not included here because there is no way
        to actually maintain an always up-to-date status.
        """
        return {"volume": self.volume, "mute": self.mute}

    def update_status(self) -> None:
        """Publishes on `MQTT_STATUS_TOPIC` the current status (volume/mute)."""
        try:
            (rc, mid) = self.mqttc.publish(
                self.config.status_topic, json.dumps(self.status), qos=0, retain=False
            )
            if rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info(
                    f"The request for a status update has been successfully accepted: mid={mid}"
                )
            else:
                logging.warning("The request for a status update has been rejected")
        except ValueError as e:
            logging.warning(f"Cannot send status update: {e}")

    def start(self) -> None:
        """Starts the MQTT client and subscribes to `MQTT_CONTROL_TOPIC` to receive commands."""
        # Set logging level
        debug_level = logging.DEBUG if self.config.debug else logging.ERROR
        logging.basicConfig(
            format="[%(asctime)s] %(levelname)-8s %(message)s", level=debug_level
        )

        try:
            # Check if authentication is required for connecting to the broker
            if self.config.user and self.config.password:
                self.mqttc.username_pw_set(
                    username=self.config.user, password=self.config.password
                )

            # Connect to the broker
            self.mqttc.connect(self.config.broker, self.config.port, keepalive=60)

            # Subscribe to the control topic, used to receive commands
            (rc, mid) = self.mqttc.subscribe(self.config.control_topic, qos=0)
            if rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info(
                    f"The request for control topic subscription has been successfully accepted: mid={mid}"
                )
            else:
                logging.warning(
                    "The request for control topic subscription has been rejected"
                )

            # Check if status updates should be sent periodically
            if self.config.status_update_delay:
                self.mqttc.loop_start()
                while True:
                    self.update_status()
                    time.sleep(self.config.status_update_delay)
            else:
                self.mqttc.loop_forever()
        except ConnectionError as e:
            logging.critical(f"Connection failed: {e}")
            sys.exit(1)
        except ValueError as e:
            logging.critical(
                f"Cannot subscribe to topic {self.config.control_topic}: {e}"
            )
            sys.exit(1)
        except Exception as e:
            logging.critical(f"Unexpected error while starting the controller: {e}")
            sys.exit(1)

    def stop(self) -> None:
        """Stops the MQTT client and disconnects from the broker."""
        self.mqttc.disconnect()


if __name__ == "__main__":
    drc = MQTTController()

    import os
    from os.path import dirname, join, exists
    from dotenv import load_dotenv

    env_path = join(join(dirname(__file__), os.pardir), ".env")
    if exists(env_path):
        load_dotenv(env_path)

    # `Config` should be imported after loading the `.env` file
    from mqttrdc.config import Config

    drc.config.from_object(Config)

    try:
        drc.start()
    finally:
        # gracefully stops the client, for example when receives a `KeyboardInterrupt` (e.g. CTRL + c)
        drc.stop()
