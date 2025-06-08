from sqlalchemy import ForeignKey

from extensions import db, sql


class ManufacturerCategorySetting(db.Model):
    __tablename__ = "manufacturer_category"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    category: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "category": self.category,
        }


class ManufacturerSetting(db.Model):
    __tablename__ = "manufacturer"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    category: db.Mapped["ManufacturerCategorySetting"] = db.mapped_column(ForeignKey(
        ManufacturerCategorySetting.id), nullable=False)
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
            "category": self.category,
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


class TankSetting(db.Model):
    __tablename__ = "tank_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    volume: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "volume": self.volume
        }


class SensorSetting(db.Model):
    __tablename__ = "sensors"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(
        ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(sql.INET, nullable=False)
    api_key: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=True)
    measuring_device: db.Mapped["TankSetting"] = db.mapped_column(ForeignKey(TankSetting.id), nullable=True)
    measuring_position: db.Mapped[str] = db.Column(db.VARCHAR(128), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "ip": self.ip,
            "api_key": self.api_key,
            "measuring_device": self.measuring_device,
            "measuring_position": self.measuring_position
        }


class PhotovoltaicSetting(db.Model):
    __tablename__ = "photovoltaic_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(
        ForeignKey(ManufacturerSetting.id), nullable=False)
    duration: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)
    angle: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)
    module_count: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)
    location: db.Mapped["LocationSetting"] = db.mapped_column(ForeignKey(LocationSetting.id), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "duration": self.duration,
            "module_count": self.module_count,
            "location": self.location,
        }


class EnergySetting(db.Model):
    __tablename__ = "energy_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(
        ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(sql.INET, nullable=False)
    api_key: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=True)
    price: db.Mapped[float] = db.Column(db.NUMERIC(10, 2), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "ip": self.ip,
            "api_key": self.api_key,
            "price": self.price,
        }


class HeatingSetting(db.Model):
    __tablename__ = "heating_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(
        ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(sql.INET, nullable=False)
    url: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=True)
    api: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=True)
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
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(
        ForeignKey(ManufacturerSetting.id), nullable=False)
    location: db.Mapped["LocationSetting"] = db.mapped_column(ForeignKey(LocationSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(sql.INET, nullable=False)
    url: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=True)
    api: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=True)
    api_key: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": f"{self.manufacturer.manufacturer} {self.manufacturer.model_type}",
            "ip": self.ip,
            "api_key": self.api_key,
            "location": self.location.description,
        }
