from sqlalchemy import ForeignKey

from extensions import db, sql


class ManufacturerCategorySetting(db.Model):
    """
    Represents a classification category for manufacturers.

    Attributes:
        id (int): Unique identifier for the category.
        description (str): Human-readable description of the category.
        category (str): Internal or technical category name.
    """
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
    """
    Represents manufacturer details including connection and configuration metadata.

    Attributes:
        id (int): Unique identifier for the manufacturer.
        description (str): Name or description of the manufacturer.
        category (ManufacturerCategorySetting): Foreign key to the manufacturer's category.
        manufacturer (str): Manufacturer name or brand.
        model_type (str): Model type identifier.
        url (str): Optional URL for accessing the manufacturer's system.
        api (str): Optional API endpoint string.
        power_factor (float): Optional power factor for calculations.
        power_size (int): Optional power rating or capacity.
        notice (str): Additional notes or metadata.
    """
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
    """
    Represents a physical location with address and GPS coordinates.

    Attributes:
        id (int): Unique identifier for the location.
        description (str): Name or description of the location.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
        city_code (int): Optional code for the city (e.g., postal code).
        city (str): Optional name of the city.
        street (str): Optional street name.
        street_number (int): Optional house or building number.
    """
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
    """
    Represents a tank configuration, such as for storing heating or water.

    Attributes:
        id (int): Unique identifier for the tank.
        description (str): Description of the tank or its use.
        volume (int): Optional volume in liters or relevant unit.
    """
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
    """
    Represents a sensor installation and its data source configuration.

    Attributes:
        id (int): Unique identifier for the sensor.
        description (str): Description of the sensor.
        manufacturer (ManufacturerSetting): Foreign key to the sensor's manufacturer.
        ip (str): IP address of the sensor device.
        api_key (str): Optional API key for accessing the sensor.
        measuring_device (TankSetting): Optional foreign key to a connected tank.
        measuring_position (str): Description of the sensor's position in the tank.
    """
    __tablename__ = "sensors"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(
        ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(db.VARCHAR(16), nullable=False)
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
    """
    Represents a photovoltaic system configuration.

    Attributes:
        id (int): Unique identifier for the configuration.
        description (str): Description of the PV system.
        manufacturer (ManufacturerSetting): Foreign key to the manufacturer.
        duration (int): Optional expected active duration (e.g. sun hours).
        angle (int): Optional mounting angle of the modules.
        module_count (int): Optional number of PV modules.
        location (LocationSetting): Foreign key to the installation location.
    """
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
    """
    Represents an energy measurement or management device.

    Attributes:
        id (int): Unique identifier for the device.
        description (str): Description of the energy system.
        manufacturer (ManufacturerSetting): Foreign key to the manufacturer.
        ip (str): IP address of the energy device.
        api_key (str): Optional API key for communication.
        price (float): Optional cost per energy unit (e.g., €/kWh).
    """
    __tablename__ = "energy_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(
        ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(db.VARCHAR(16), nullable=False)
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
    """
    Represents a heating system configuration.

    Attributes:
        id (int): Unique identifier for the heating system.
        description (str): Description of the heating system.
        manufacturer (ManufacturerSetting): Foreign key to the manufacturer.
        ip (str): IP address of the heating device.
        api_key (str): Optional API key for remote access.
        buffer (int): Optional buffer capacity or identifier.
    """
    __tablename__ = "heating_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(
        ForeignKey(ManufacturerSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(db.VARCHAR(16), nullable=False)
    api_key: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=True)
    buffer: db.Mapped[int] = db.Column(db.INTEGER, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "ip": self.ip,
            "api_key": self.api_key,
            "buffer": self.buffer
        }


class WeatherSetting(db.Model):
    """
    Represents a weather data source or sensor system.

    Attributes:
        id (int): Unique identifier for the weather system.
        description (str): Description of the system or station.
        manufacturer (ManufacturerSetting): Foreign key to the manufacturer.
        location (LocationSetting): Foreign key to the station's location.
        ip (str): IP address of the weather device.
        api_key (str): Optional API key for weather data access.
    """
    __tablename__ = "weather_settings"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    description: db.Mapped[str] = db.Column(db.VARCHAR(256), nullable=False)
    manufacturer: db.Mapped["ManufacturerSetting"] = db.mapped_column(
        ForeignKey(ManufacturerSetting.id), nullable=False)
    location: db.Mapped["LocationSetting"] = db.mapped_column(ForeignKey(LocationSetting.id), nullable=False)
    ip: db.Mapped[str] = db.Column(db.VARCHAR(16), nullable=False)
    api_key: db.Mapped[str] = db.Column(db.VARCHAR(512), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "ip": self.ip,
            "api_key": self.api_key,
            "location": self.location,
        }
