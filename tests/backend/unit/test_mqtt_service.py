from unittest.mock import MagicMock, patch

from function.backend.services.mqtt_service import MQTTService


@patch("function.backend.services.mqtt_service.mqtt.Client")
def test_mqtt_connect(mock_mqtt_client):
    """Testet ob der Connect-Flow aufgerufen wird"""
    mock_client_instance = MagicMock()
    mock_mqtt_client.return_value = mock_client_instance

    service = MQTTService(broker="localhost", port=1883)
    service.connect()

    mock_client_instance.connect.assert_called_once_with("localhost", 1883, 60)
    mock_client_instance.loop_start.assert_called_once()


@patch("function.backend.services.mqtt_service.mqtt.Client")
def test_mqtt_publish(mock_mqtt_client):
    """Testet Publish auf ein Topic"""
    mock_client_instance = MagicMock()
    mock_mqtt_client.return_value = mock_client_instance

    service = MQTTService()
    service.client = mock_client_instance
    service.publish("test/topic", "payload")

    mock_client_instance.publish.assert_called_once_with("test/topic", "payload")


@patch("function.backend.services.mqtt_service.mqtt.Client")
def test_mqtt_subscribe(mock_mqtt_client):
    """Testet Subscribe auf ein Topic"""
    mock_client_instance = MagicMock()
    mock_mqtt_client.return_value = mock_client_instance

    service = MQTTService()
    service.client = mock_client_instance
    service.subscribe("test/topic")

    mock_client_instance.subscribe.assert_called_once_with("test/topic")
