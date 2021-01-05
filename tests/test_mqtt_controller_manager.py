from unittest import TestCase
from mqttrdc.mqtt_controller_manager import MQTTControllerManager


class FakeConfig:
    KEY1 = "value1"
    KEY2 = 10
    key3 = 20


class TestControllerManagerSetup(TestCase):
    def test_from_object(self):
        manager = MQTTControllerManager()
        manager.from_object(FakeConfig)
        expected = {"KEY1": "value1", "KEY2": 10}
        self.assertEqual(expected, manager)


class TestBrokerAddrConfig(TestCase):
    def test_broker_addr_not_found(self):
        manager = MQTTControllerManager()
        self.assertRaises(KeyError, lambda: manager.broker)

    def test_broker_addr_not_valid(self):
        for broker_addr in ("", None):
            manager = MQTTControllerManager(MQTT_BROKER_ADDR=broker_addr)
            self.assertRaises(ValueError, lambda: manager.broker)

    def test_broker_addr_valid(self):
        manager = MQTTControllerManager(MQTT_BROKER_ADDR="127.0.0.1")
        self.assertEqual("127.0.0.1", manager.broker)


class TestBrokerPortConfig(TestCase):
    def test_broker_port_not_found(self):
        manager = MQTTControllerManager()
        self.assertRaises(KeyError, lambda: manager.port)

    def test_broker_port_not_valid(self):
        manager = MQTTControllerManager(MQTT_BROKER_PORT="")
        self.assertRaises(ValueError, lambda: manager.port)

        manager = MQTTControllerManager(MQTT_BROKER_PORT=None)
        self.assertRaises(TypeError, lambda: manager.port)

    def test_broker_port_valid(self):
        for broker_port in ("1883", 1883):
            manager = MQTTControllerManager(MQTT_BROKER_PORT=broker_port)
            self.assertEqual(1883, manager.port)


class TestBrokerUserConfig(TestCase):
    def test_broker_user_not_found(self):
        manager = MQTTControllerManager()
        self.assertEqual(None, manager.user)

    def test_broker_user_not_valid(self):
        for broker_user in (None, 1):
            manager = MQTTControllerManager(MQTT_BROKER_USER=broker_user)
            self.assertRaises(ValueError, lambda: manager.user)

    def test_broker_user_valid(self):
        manager = MQTTControllerManager(MQTT_BROKER_USER="user")
        self.assertEqual("user", manager.user)


class TestBrokerPasswordConfig(TestCase):
    def test_broker_password_not_found(self):
        manager = MQTTControllerManager()
        self.assertEqual(None, manager.password)

    def test_broker_password_not_valid(self):
        for broker_password in (None, 1):
            manager = MQTTControllerManager(MQTT_BROKER_PWD=broker_password)
            self.assertRaises(ValueError, lambda: manager.password)

    def test_broker_user_valid(self):
        manager = MQTTControllerManager(MQTT_BROKER_PWD="password")
        self.assertEqual("password", manager.password)


class TestControlTopicConfig(TestCase):
    def test_control_topic_not_found(self):
        manager = MQTTControllerManager()
        self.assertRaises(KeyError, lambda: manager.control_topic)

    def test_control_topic_not_valid(self):
        for control_topic in ("", None):
            manager = MQTTControllerManager(MQTT_CONTROL_TOPIC=control_topic)
            self.assertRaises(ValueError, lambda: manager.control_topic)

    def test_control_topic_valid(self):
        manager = MQTTControllerManager(MQTT_CONTROL_TOPIC="desktop/control")
        self.assertEqual("desktop/control", manager.control_topic)


class TestStatusTopicConfig(TestCase):
    def test_status_topic_not_found(self):
        manager = MQTTControllerManager()
        self.assertRaises(KeyError, lambda: manager.status_topic)

    def test_status_topic_not_valid(self):
        for status_topic in ("", None):
            manager = MQTTControllerManager(MQTT_STATUS_TOPIC=status_topic)
            self.assertRaises(ValueError, lambda: manager.status_topic)

    def test_status_topic_valid(self):
        manager = MQTTControllerManager(MQTT_STATUS_TOPIC="desktop/status")
        self.assertEqual("desktop/status", manager.status_topic)


class TestVolumeStepConfig(TestCase):
    def test_volume_step_not_found(self):
        manager = MQTTControllerManager()
        self.assertEqual(10, manager.volume_step)

    def test_volume_step_not_valid(self):
        manager = MQTTControllerManager(VOLUME_STEP="")
        self.assertRaises(ValueError, lambda: manager.volume_step)

        manager = MQTTControllerManager(VOLUME_STEP=None)
        self.assertRaises(TypeError, lambda: manager.volume_step)

        for volume_step in (-1, 0, 101):
            manager = MQTTControllerManager(VOLUME_STEP=volume_step)
            self.assertRaises(ValueError, lambda: manager.volume_step)

    def test_volume_step_valid(self):
        for volume_step in range(1, 101):
            manager = MQTTControllerManager(VOLUME_STEP=volume_step)
            self.assertEqual(volume_step, manager.volume_step)

            manager = MQTTControllerManager(VOLUME_STEP=str(volume_step))
            self.assertEqual(volume_step, manager.volume_step)


class TestStatusUpdateDelayConfig(TestCase):
    def test_status_update_delay_not_found(self):
        manager = MQTTControllerManager()
        self.assertEqual(None, manager.status_update_delay)

    def test_status_update_delay_not_valid(self):
        manager = MQTTControllerManager(STATUS_UPDATE_DELAY="")
        self.assertRaises(ValueError, lambda: manager.status_update_delay)

        manager = MQTTControllerManager(STATUS_UPDATE_DELAY=None)
        self.assertRaises(TypeError, lambda: manager.status_update_delay)

        for status_update_delay in (-1, "-1"):
            manager = MQTTControllerManager(STATUS_UPDATE_DELAY=status_update_delay)
            self.assertRaises(ValueError, lambda: manager.status_update_delay)

    def test_status_update_delay_valid(self):
        for status_update_delay in (0, 10):
            manager = MQTTControllerManager(STATUS_UPDATE_DELAY=status_update_delay)
            self.assertEqual(status_update_delay, manager.status_update_delay)

            manager = MQTTControllerManager(
                STATUS_UPDATE_DELAY=str(status_update_delay)
            )
            self.assertEqual(status_update_delay, manager.status_update_delay)


class TestDebugConfig(TestCase):
    def test_debug_not_found(self):
        manager = MQTTControllerManager()
        self.assertEqual(False, manager.debug)

    def test_debug_valid(self):
        for debug in (True, "1", "10", 1, 10):
            manager = MQTTControllerManager(DEBUG=debug)
            self.assertEqual(True, manager.debug)

        for debug in (False, "", 0):
            manager = MQTTControllerManager(DEBUG=debug)
            self.assertEqual(False, manager.debug)
