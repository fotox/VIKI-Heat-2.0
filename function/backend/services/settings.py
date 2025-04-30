from sqlalchemy import ForeignKey
from typing import List

from extensions import db


class PhotovoltaicSetting(db.Model):
    __tablename__ = "photovoltaic_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    system_id: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    duration: db.Mapped[int] = db.Column(db.Integer, nullable=True)
    angle: db.Mapped[int] = db.Column(db.Integer, nullable=True)
    max_output: db.Mapped[int] = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "duration": self.duration,
            "angle": self.angle,
            "max_output": self.max_output,
        }


class ManufacturerSetting(db.Model):
    __tablename__ = "manufacturer_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    system_id: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    description: db.Mapped[int] = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "description": self.description,
        }


class ElectricityProviderSetting(db.Model):
    __tablename__ = "electricity_provider_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    system_id: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    provider: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    ip: db.Mapped[str] = db.Column(db.String(16), nullable=True)
    url: db.Mapped[str] = db.Column(db.String(256), nullable=True)
    api: db.Mapped[str] = db.Column(db.String(256), nullable=True)
    selected: db.Mapped[str] = db.Column(db.String(256), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "manufacturer": self.manufacturer,
            "ip": self.ip,
            "url": self.url,
            "api": self.api,
            "selected": self.selected,
        }


class EnergySetting(db.Model):
    __tablename__ = "energy_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    system_id: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(db.String(16), nullable=True)
    url: db.Mapped[str] = db.Column(db.String(256), nullable=True)
    battery_api: db.Mapped[str] = db.Column(db.String(256), nullable=True)
    feed_in_api: db.Mapped[str] = db.Column(db.String(256), nullable=True)
    production_api: db.Mapped[str] = db.Column(db.String(256), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "manufacturer": self.manufacturer,
            "ip": self.ip,
            "url": self.url,
            "battery_api": self.battery_api,
            "feed_in_api": self.feed_in_api,
            "production_api": self.production_api,
        }


class HeatingModeSetting(db.Model):
    __tablename__ = "heating_mode_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    system_id: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    description: db.Mapped[int] = db.Column(db.Integer, nullable=True)
    selected: db.Mapped[bool] = db.Column(db.Boolean, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "description": self.description,
            "selected": self.selected,
        }


class HeatingSetting(db.Model):
    __tablename__ = "heating_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    system_id: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    manufacturer: db.Mapped[str] = db.Column(db.String(64), nullable=True)
    api: db.Mapped[str] = db.Column(db.String(256), nullable=True)
    ip: db.Mapped[str] = db.Column(db.String(16), nullable=True)
    url: db.Mapped[str] = db.Column(db.String(256), nullable=True)
    price: db.Mapped[float] = db.Column(db.Double, nullable=True)
    power_factor: db.Mapped[float] = db.Column(db.Double, nullable=True)
    selected: db.Mapped[int] = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "manufacturer": self.manufacturer,
            "api": self.api,
            "ip": self.ip,
            "url": self.url,
            "price": self.price,
            "power_factor": self.power_factor,
            "selected": self.selected,
        }


class WeatherSetting(db.Model):
    __tablename__ = "weather_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    system_id: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    provider: db.Mapped[str] = db.Column(db.String(64), nullable=True)
    api: db.Mapped[str] = db.Column(db.String(256), nullable=True)
    ip: db.Mapped[str] = db.Column(db.String(16), nullable=True)
    url: db.Mapped[str] = db.Column(db.String(256), nullable=True)
    selected: db.Mapped[int] = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "provider": self.provider,
            "api": self.api,
            "ip": self.ip,
            "url": self.url,
            "selected": self.selected,
        }


class TankSetting(db.Model):
    __tablename__ = "tank_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    system_id: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    description: db.Mapped[str] = db.Column(db.String(64), nullable=True)
    capacity: db.Mapped[int] = db.Column(db.Integer, nullable=True)
    destination_temp: db.Mapped[int] = db.Column(db.Integer, nullable=True)
    heating_element: db.Mapped[bool] = db.Column(db.Boolean, nullable=True)
    temp_sensors: db.Mapped[List["TempSensorSetting"]] = db.relationship(back_populates="tank")
    legionellen_days: db.Mapped[int] = db.Column(db.Integer, nullable=True)
    legionellen_temp: db.Mapped[int] = db.Column(db.Integer, nullable=True)
    legionellen_enabled: db.Mapped[bool] = db.Column(db.Boolean, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "description": self.description,
            "capacity": self.capacity,
            "destination_temp": self.destination_temp,
            "heating_element": self.heating_element,
            "temp_sensors": self.temp_sensors,
            "legionellen_days": self.legionellen_days,
            "legionellen_temp": self.legionellen_temp,
            "legionellen_enabled": self.legionellen_enabled,
        }


class TempSensorSetting(db.Model):
    __tablename__ = "temp_sensor_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    system_id: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    description: db.Mapped[str] = db.Column(db.String(64), nullable=True)
    tank_id: db.Mapped[int] = db.mapped_column(ForeignKey("tank_settings.id"))
    tank: db.Mapped["TankSetting"] = db.relationship(back_populates="temp_sensors")
    tank_binding: db.Mapped[str] = db.Column(db.String(64), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "description": self.description,
            "tank_id": self.tank_id,
            "tank": self.tank,
            "tank_binding": self.tank_binding,
        }


class LocationSetting(db.Model):
    __tablename__ = "location_settings"

    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    city: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    latitude: db.Mapped[float] = db.Column(db.Double, nullable=True)
    longitude: db.Mapped[float] = db.Column(db.Double, nullable=True)
    street: db.Mapped[str] = db.Column(db.String(64), nullable=False)
    street_number: db.Mapped[int] = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "street": self.street,
            "street_number": self.street_number,
        }
