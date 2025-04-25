"""
Verbindung zu einem MQTT-Broker zum Senden und Empfangen von Nachrichten.
"""

import paho.mqtt.client as mqtt
from typing import Callable, Optional


class MQTTService:
    def __init__(self, broker: str = "localhost", port: int = 1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self._on_message: Optional[Callable] = None

    def connect(self) -> None:
        """Stellt Verbindung zum MQTT-Broker her"""
        self.client.on_connect = self._on_connect
        if self._on_message:
            self.client.on_message = self._on_message
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        print(f"[MQTT] Verbunden mit {self.broker}:{self.port}")

    def _on_connect(self, client, userdata, flags, rc) -> None:
        print(f"[MQTT] Connected mit Result Code: {rc}")

    def publish(self, topic: str, payload: str) -> None:
        """Sendet eine Nachricht an ein Topic"""
        self.client.publish(topic, payload)
        print(f"[MQTT] Published: {topic} → {payload}")

    def subscribe(self, topic: str) -> None:
        """Abonniert ein Topic"""
        self.client.subscribe(topic)
        print(f"[MQTT] Subscribed: {topic}")

    def set_on_message_callback(self, callback: Callable) -> None:
        """Definiert Callback für eingehende Nachrichten"""
        self._on_message = callback
        self.client.on_message = callback
