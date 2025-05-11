from extensions import db, sql


class DashboardModuleSetting(db.Model):
    __tablename__ = "dashboard_modules"

    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER, nullable=False)
    module_type = db.Column(db.VARCHAR(50), nullable=False)
    position = db.Column(db.INTEGER, nullable=False, default=0)
