from extensions import db


class PhotovoltaicSetting(db.Model):
    __tablename__ = "photovoltaic_settings"
    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.String(64), nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    angle = db.Column(db.Integer, nullable=True)
    max_output = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "duration": self.duration,
            "angle": self.angle,
            "max_output": self.max_output,
        }
