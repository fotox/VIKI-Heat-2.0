from sqlalchemy import ForeignKey

from extensions import db, sql


class ManufacturerSetting(db.Model):
    __tablename__ = "manufacturer"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    model_type: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    url: db.Mapped[int] = db.Column(db.VARCHAR(256), nullable=True)
    api: db.Mapped[int] = db.Column(db.VARCHAR(256), nullable=True)
    power_factor: db.Mapped[float] = db.Column(db.NUMERIC(3, 2), nullable=True)
    power_size: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)
    notice: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "model_type": self.model_type,
            "url": self.url,
            "api": self.api,
            "power_factor": self.power_factor,
            "power_size": self.power_size,
        }


class LocationSetting(db.Model):
    __tablename__ = "location"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    latitude: db.Mapped[float] = db.Column(db.NUMERIC(9, 5), nullable=False)
    longitude: db.Mapped[float] = db.Column(db.NUMERIC(9, 5), nullable=False)
    city_code: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)
    city: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=True)
    street: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=True)
    street_number: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_code": self.city_code,
            "city": self.city,
            "street": self.street,
            "street_number": self.street_number,
        }


class ApiSetting(db.Model):
    __tablename__ = "api"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    api: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "api": self.api,
        }


class UrlSetting(db.Model):
    __tablename__ = "url"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    url: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "url": self.url,
        }


class SensorSetting(db.Model):
    __tablename__ = "sensors"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(sql.INET, nullable=False)
    url: db.Mapped["UrlSetting"] = db.mapped_column(ForeignKey(UrlSetting.id), nullable=True)
    api: db.Mapped["ApiSetting"] = db.mapped_column(ForeignKey(ApiSetting.id), nullable=True)
    api_key: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": f"{self.manufacturer.manufacturer} {self.manufacturer.model_type}",
            "ip": self.ip,
            "url": self.url.url,
            "api": self.api.api,
            "api_key": self.api_key,
        }


class PhotovoltaicSetting(db.Model):
    __tablename__ = "photovoltaic_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(ForeignKey(ManufacturerSetting.id), nullable=False)
    duration: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)
    angle: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)
    module_count: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)
    location: db.Mapped["LocationSetting"] = db.mapped_column(ForeignKey(LocationSetting.id), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": f"{self.manufacturer.manufacturer} {self.manufacturer.model_type}",
            "duration": self.duration,
            "module_count": self.module_count,
            "location": self.manufacturer.description,
        }


class EnergySetting(db.Model):
    __tablename__ = "energy_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(sql.INET, nullable=False)
    api_key: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=True)
    price: db.Mapped[float] = db.Column(db.NUMERIC(10, 2), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "manufacturer": self.manufacturer,
            "ip": self.ip,
            "api_key": self.api_key,
            "price": self.price,
        }


class HeatingSetting(db.Model):
    __tablename__ = "heating_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(sql.INET, nullable=False)
    api_key: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "ip": self.ip,
            "api_key": self.api_key,
        }


class WeatherSetting(db.Model):
    __tablename__ = "weather_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(ForeignKey(ManufacturerSetting.id), nullable=False)
    location: db.Mapped["LocationSetting"] = db.mapped_column(ForeignKey(LocationSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(sql.INET, nullable=False)
    url: db.Mapped["UrlSetting"] = db.mapped_column(ForeignKey(UrlSetting.id), nullable=True)
    api: db.Mapped["ApiSetting"] = db.mapped_column(ForeignKey(ApiSetting.id), nullable=True)
    api_key: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": f"{self.manufacturer.manufacturer} {self.manufacturer.model_type}",
            "ip": self.ip,
            "url": self.url.url,
            "api": self.api.api,
            "api_key": self.api_key,
            "location": self.location.description,
        }


class TankSetting(db.Model):
    __tablename__ = "tank_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    volume: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)
    sensors: db.Mapped["SensorSetting"] = db.mapped_column(ForeignKey(SensorSetting.id), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "volume": self.volume,
            "sensors": self.sensors.description,
        }
