from function.backend.services.sensor_service import SensorService


def test_read_temperature_returns_none_for_invalid_sensor():
    sensor_service = SensorService(base_dir="/invalid/path/")
    assert sensor_service.read_temperature("fake_id") is None
