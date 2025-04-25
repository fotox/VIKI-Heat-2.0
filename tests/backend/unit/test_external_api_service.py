from function.backend.services.external_api_service import WeatherService, SolarForecastService, TibberService
from unittest.mock import patch


# WeatherService Tests
@patch("services.external_api_service.requests.get")
def test_weather_service_success(mock_get):
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {"main": {"temp": 20}}

    service = WeatherService(api_key="dummy")
    data = service.get_weather()
    assert data["main"]["temp"] == 20


@patch("services.external_api_service.requests.get")
def test_weather_service_failure(mock_get):
    mock_get.return_value.ok = False

    service = WeatherService(api_key="dummy")
    data = service.get_weather()
    assert data is None


# SolarForecastService Tests
@patch("services.external_api_service.requests.get")
def test_solar_forecast_service_success(mock_get):
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {"forecast": "ok"}

    service = SolarForecastService()
    data = service.get_forecast(system_id="test-id")
    assert data["forecast"] == "ok"


# TibberService Tests
@patch("services.external_api_service.requests.post")
def test_tibber_service_success(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {"viewer": "data"}

    service = TibberService(token="dummy")
    data = service.get_home_data()
    assert data["viewer"] == "data"
