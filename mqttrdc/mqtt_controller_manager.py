"""MQTT Remote Desktop Controller Manager.

Used to handle the user configurations.
"""
from typing import Optional


class MQTTControllerManager(dict):
    """A class used to manage the configurations needed by `MQTTController`."""

    def from_object(self, obj: object) -> None:
        """Loads the configurations from an object."""
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    @property
    def broker(self) -> str:
        """Gets the broker address, `MQTT_BROKER_ADDR`, from the configuration.

        Returns
        -------
        str
            the MQTT broker address

        Raises
        ------
        KeyError
            if `MQTT_BROKER_ADDR` does not exist in the configuration
        ValueError
            if `MQTT_BROKER_ADDR` is not a string or is an empty string
        """
        mqtt_broker_addr = self["MQTT_BROKER_ADDR"]
        if isinstance(mqtt_broker_addr, str) and mqtt_broker_addr:
            return mqtt_broker_addr
        else:
            raise ValueError("'MQTT_BROKER_ADDR' should be a not empty string")

    @property
    def port(self) -> int:
        """Gets the broker port, `MQTT_BROKER_PORT`, from the configuration.

        Returns
        -------
        int
            the MQTT broker port

        Raises
        ------
        KeyError
            if `MQTT_BROKER_PORT` does not exist in the configuration
        TypeError
            if `MQTT_BROKER_PORT` is not a string, a bytes-like object or a number
        ValueError
            if `MQTT_BROKER_PORT` is not a valid integer literal
        """
        return int(self["MQTT_BROKER_PORT"])

    @property
    def user(self) -> Optional[str]:
        """Gets the user, `MQTT_BROKER_USER`, from the configuration.

        A user is needed when broker connection requires authentication.

        Returns
        -------
        Optional[str]
            the user if exists in the configuration, `None` otherwise

        Raises
        ------
        ValueError
            if `MQTT_BROKER_USER` is not a valid string literal
        """
        if "MQTT_BROKER_USER" in self:
            if isinstance(self["MQTT_BROKER_USER"], str):
                return self["MQTT_BROKER_USER"]
            else:
                raise ValueError("'MQTT_BROKER_USER' should be a string")
        else:
            return None

    @property
    def password(self) -> Optional[str]:
        """Gets the user's password, `MQTT_BROKER_PWD`, from the configuration.

        A user's password is needed when broker connection requires authentication.

        Returns
        -------
        Optional[str]
            the password if exists in the configuration, `None` otherwise

        Raises
        ------
        ValueError
            if `MQTT_BROKER_PWD` is not a valid string literal
        """
        if "MQTT_BROKER_PWD" in self:
            if isinstance(self["MQTT_BROKER_PWD"], str):
                return self["MQTT_BROKER_PWD"]
            else:
                raise ValueError("'MQTT_BROKER_PWD' should be a string")
        else:
            return None

    @property
    def control_topic(self) -> str:
        """Gets the control topic, `MQTT_CONTROL_TOPIC`, from the configuration.

        The control topic is used by the client to receive commands from the user.

        Returns
        -------
        str
            the MQTT control topic

        Raises
        ------
        KeyError
            if `MQTT_CONTROL_TOPIC` does not exist in the configuration
        ValueError
            if `MQTT_CONTROL_TOPIC` is not a string or is an empty string
        """
        mqtt_control_topic = self["MQTT_CONTROL_TOPIC"]
        if isinstance(mqtt_control_topic, str) and mqtt_control_topic:
            return mqtt_control_topic
        else:
            raise ValueError("'MQTT_CONTROL_TOPIC' should be a not empty string")

    @property
    def status_topic(self) -> str:
        """Gets the status topic, `MQTT_STATUS_TOPIC`, from the configuration.

        The status topic is used by the client to send status updates to the user.

        Returns
        -------
        str
            the MQTT status topic

        Raises
        ------
        KeyError
            if `MQTT_STATUS_TOPIC` does not exist in the configuration
        ValueError
            if `MQTT_STATUS_TOPIC` is not a string or is an empty string
        """
        mqtt_status_topic = self["MQTT_STATUS_TOPIC"]
        if isinstance(mqtt_status_topic, str) and mqtt_status_topic:
            return mqtt_status_topic
        else:
            raise ValueError("'MQTT_STATUS_TOPIC' should be a not empty string")

    @property
    def volume_step(self) -> int:
        """Gets the volume step, `VOLUME_STEP`, from the configuration.

        Volume controls, like increment and decrement, act on the volume according to this value.

        Returns
        -------
        int
            the volume step value if provided in the configuration, `10` otherwise

        Raises
        ------
        TypeError
            if `VOLUME_STEP` is not a string, a bytes-like object or a number
        ValueError
            if `VOLUME_STEP` is not a valid integer literal; or it's not a value between 1 and 100, extremes included
        """
        if "VOLUME_STEP" in self:
            volume_step = int(self["VOLUME_STEP"])
            if volume_step in range(1, 101):
                return volume_step
            else:
                raise ValueError(
                    "'VOLUME_STEP' must be a value between 1 and 100, extremes included"
                )
        else:
            return 10

    @property
    def status_update_delay(self) -> Optional[int]:
        """Gets the value of the frequency of status updates, `STATUS_UPDATE_DELAY`, from the configuration.

        If this is enabled, meaning a value is specified in the configuration, the client publishes a status
        update to the `MQTT_STATUS_TOPIC` every `STATUS_UPDATE_DELAY` seconds. if not enabled, status updates
        are published only when the user act upon the volume with the corresponding commands.

        Returns
        -------
        Optional[str]
            the status update delay if provided in the configuration, `None` otherwise

        Raises
        ------
        TypeError
            if `STATUS_UPDATE_DELAY` is not a string, a bytes-like object or a number
        ValueError
            if `STATUS_UPDATE_DELAY` is not a valid, non-negative, integer literal
        """
        if "STATUS_UPDATE_DELAY" in self:
            status_update_delay = int(self["STATUS_UPDATE_DELAY"])
            if status_update_delay >= 0:
                return status_update_delay
            else:
                raise ValueError("'STATUS_UPDATE_DELAY' must be non-negative")
        else:
            return None

    @property
    def debug(self) -> bool:
        """Gets the debug mode, `DEBUG`, from the configuration.

        When debug mode is enabled, the user will get information about the execution;
        otherwise, only the errors will be logged.

        Returns
        -------
        bool
            whether the debug mode is enabled or not; by default it is not enabled
        """
        return bool(self.get("DEBUG", False))
