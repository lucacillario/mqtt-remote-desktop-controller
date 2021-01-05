"""MQTT Remote Desktop Controller.

This package contains some useful tools that allow the user to remotely control multimedia functions of his
desktop/laptop, through the MQTT protocol.

The main purpose of the project is to allow remote control of applications such as Netflix, Prime Video, Disney +,
Spotify etc ...

It provides the following classes:

1. `MQTTController`: the actual MQTT controller, that receives commands from the user and notify of status updates.
2. `MQTTControllerManager`: the configuration manager, that handles all the user configurations.
3. `Config`: the configuration object containing the actual configuration parameters.
"""
