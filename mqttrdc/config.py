"""MQTT Remote Desktop Controller Configurations.
"""
import os
from typing import Optional, Union


class Config:
    """User configurations.

    Attributes
    ----------
    MQTT_BROKER_ADDR: str
        The MQTT broker address
    MQTT_BROKER_PORT: Union[str, int]
        The MQTT broker port
    MQTT_BROKER_USER: Optional[str]
        The MQTT broker user (default=None)
    MQTT_BROKER_PWD: Optional[str]
        The MQTT broker password (default=None)
    MQTT_CONTROL_TOPIC: str
        The MQTT control topic, used by the application to receive user commands
    MQTT_STATUS_TOPIC: str
        The MQTT status topic, used by the application to notify the user of status updates (volume/mute)
    VOLUME_STEP: Optional[int]
        How much to increase / decrease the volume (default=10)
    STATUS_UPDATE_DELAY: Optional[int]
        How much seconds between automatic status updates (default=None, automatic status updates are disabled)
    DEBUG: Optional[bool]
        Whether to activate debug mode or not (default=False)
    """

    MQTT_BROKER_ADDR = os.environ.get("MQTT_BROKER_ADDR")
    MQTT_BROKER_PORT = os.environ.get("MQTT_BROKER_PORT")
    MQTT_BROKER_USER = os.environ.get("MQTT_BROKER_USER")
    MQTT_BROKER_PWD = os.environ.get("MQTT_BROKER_PWD")
    MQTT_CONTROL_TOPIC = os.environ.get("MQTT_CONTROL_TOPIC")
    MQTT_STATUS_TOPIC = os.environ.get("MQTT_STATUS_TOPIC")
    # VOLUME_STEP = 5
    # STATUS_UPDATE_DELAY = 30
    # DEBUG = True
