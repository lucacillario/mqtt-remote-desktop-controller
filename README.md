![Python package](https://github.com/lucacillario/mqtt-remote-desktop-controller/workflows/Python%20package/badge.svg)

This project allows you to remotely control some multimedia functionalities 
of your desktop/laptop, through the MQTT protocol.

You will be able to control the volume, mute/unmute, play/pause and skip forward/backward your
content (Netflix, Prime Video, Disney+, Spotify and many more) comfortably 
from your sofa.

To be clear, this is just a client that exposes some of your pc's 
functionalities via MQTT, you will still need a remote control or 
something similar to send the commands. 
I myself integrated it with [Home Assistant](https://www.home-assistant.io/) 
and use it with a [Osram Smart+ Mini Switch](https://i.imgur.com/lAiCZMS.jpg).

At this point you may be wondering "Why not buy a PC remote control directly?".
Well, you might be right but consider this:
- many of them suck with Linux
- have way more functionalities than you might need, and the ones you need may not work well
- they are not as customizable
- last but not least, it's not as fun as building a custom remote control! 🤓
  

# How it works

![Imgur](https://i.imgur.com/L8lNica.png)

There are three main parties involved:
- a device compatible with MQTT able to send commands (e.g. a remote control)
- your pc, in which this project runs (from now on aka *the client*)
- an MQTT broker, used to connect the two

The broker, which might be running either locally on your pc or somewhere else, 
handles two topics: a **control topic** and a **status topic**.
The MQTT compatible remote control sends commands to the control topic, these
are received by the client that is subscribed to it, executed, and the results
are sent back to the broker via the status topic, which can be subsequently
consumed.

This is clearly a simplification of the overall functioning of the system.
In a real case scenario it is very unlikely that a remote control will be
able to send commands directly to an MQTT broker. 

In my case, I use a Zigbee remote integrated with Home Assistant. 
Home Assistant based on the button pressed, publish a message to the control
topic. This is received by the client, executed, and the result is sent back
to the status topic, where Home Assistant consumes it and keeps a status 
dashboard up-to-date.


# Setup

- Clone the repository
- Create and activate a virtual environment (optional)
- Install the project dependencies:
```shell
make install
```
> This project requires **pyalsaaudio**, and you might need to install
> some dependencies on you OS before to install it. [Check out the doc](https://larsimmisch.github.io/pyalsaaudio/pyalsaaudio.html#installation).
> On Debian (and Ubuntu), install **libasound2-dev**.

- Set up the project configuration parameters:

|         Name        |   Type   | Optional | Default |      Examples     |                     Description                    |
|:-------------------:|:--------:|:--------:|:-------:|:-----------------:|:--------------------------------------------------:|
|    MQTT_BROKER_ADDR |    str   |    No    |         |    '127.0.0.1'    | The MQTT Broker address                            |
|    MQTT_BROKER_PORT | str, int |    No    |         |   '1883'<br>1883  | The MQTT Broker port                               |
|    MQTT_BROKER_USER |    str   |    Yes   |   None  |       'user'      | The MQTT Broker user, if broker requires auth      |
|     MQTT_BROKER_PWD |    str   |    Yes   |   None  |     'password'    | The MQTT Broker password, if broker requires auth  |
|  MQTT_CONTROL_TOPIC |    str   |    No    |         | 'desktop/control' | The MQTT control topic, used to receive commands   |
|   MQTT_STATUS_TOPIC |    str   |    No    |         |  'desktop/status' | The MQTT status topic, used to send status updates |
|         VOLUME_STEP |    int   |    Yes   |    10   |         20        | How much to increase / decrease the volume (%)     |
| STATUS_UPDATE_DELAY |    int   |    Yes   |   None  |         30        | How much seconds between automatic status updates  |
|               DEBUG |   bool   |    Yes   |  False  |   True<br>False   | Whether to activate debug mode or not              |

You can set the mandatory configuration parameters by either creating an `.env` file in the
project's root directory:
```shell
MQTT_BROKER_ADDR='127.0.0.1'
MQTT_BROKER_PORT='1883'
MQTT_BROKER_USER='mqtt_user'
MQTT_BROKER_PWD='mqtt_password'
MQTT_CONTROL_TOPIC='desktop/control'
MQTT_STATUS_TOPIC='desktop/status'
```

or by manually configuring the module [config.py](mqttrdc/config.py).


# Usage

Inside the project's root directory:

```shell
make install
```
Install the project dependencies.

```shell
make test
```
Run tests.

```shell
make docker
```
Run a Docker `Mosquitto` instance, binding port `1883:1883` .

```shell
make run
```
Run the project and start the MQTT client.

```shell
make doc
```
Generate the project documentation.

```shell
make show-doc
```
Start a pdoc server on `http://localhost:8080` to browse the documentation.

# Available commands
Below are examples of commands you can publish to `MQTT_CONTROL_TOPIC`,
in JSON format:

```json
{"volume": 100}
```
Sets the volume to 100%.

```json
{"volumeCtrl": "+"}
```
```json
{"volumeCtrl": "-"}
```
Increases and decreases the volume by `VOLUME_STEP`.

```json
{"mute": true}
```
```json
{"mute": false}
```
Mute and unmute.

```json
{"toggle": "mute"}
```
```json
{"toggle": "pause"}
```
Toggle mute/unmute and play/pause.

```json
{"ctrl": ">>"}
```
```json
{"ctrl": "<<"}
```
Skip forward/backward.


# Notes
Toggle play/pause and skip forward/backward requires the focus to be on the target window.
These commands work by taking advantage of the platform's keyboard shortcuts:
- `Space bar` play/pause
- `Arrow right/left` skip forward/backward

Make sure the application you want to control supports these shortcuts!
