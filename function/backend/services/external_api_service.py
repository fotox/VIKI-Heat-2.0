"""
Externe API-Zugriffe: Wetter, Solar-Forecast, Tibber etc.
"""

import requests
from typing import Optional


class WeatherService:
    def __init__(self, api_key: str, location: str = "Berlin", unit: str = "metric"):
        self.api_key = api_key
        self.location = location
        self.unit = unit
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self) -> Optional[dict]:
        """Holt aktuelle Wetterdaten von OpenWeatherMap"""
        try:
            response = requests.get(self.base_url, params={
                "q": self.location,
                "units": self.unit,
                "appid": self.api_key
            })
            if response.ok:
                return response.json()
            return None
        except Exception as e:
            print(f"[Weather] Fehler beim Abrufen: {e}")
            return None


class SolarForecastService:
    def __init__(self, url: str = "https://api.solar.sheenl.de/forecast"):
        self.url = url

    def get_forecast(self, system_id: str) -> Optional[dict]:
        """Lädt Forecast-Daten für eine PV-Anlage"""
        try:
            response = requests.get(f"{self.url}?system_id={system_id}")
            if response.ok:
                return response.json()
            return None
        except Exception as e:
            print(f"[Forecast] Fehler: {e}")
            return None


class TibberService:
    def __init__(self, token: str):
        self.token = token
        self.api_url = "https://api.tibber.com/v1-beta/gql"

    def get_home_data(self) -> Optional[dict]:
        """Ruft Energiedaten von Tibber ab"""
        query = """
        {
            viewer {
                homes {
                    currentSubscription {
                        priceInfo {
                            current {
                                total
                                energy
                                tax
                            }
                        }
                    }
                }
            }
        }
        """
        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.token}"},
                json={"query": query}
            )
            if response.ok:
                return response.json()
            return None
        except Exception as e:
            print(f"[Tibber] Fehler: {e}")
            return None
