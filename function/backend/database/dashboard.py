from extensions import db


class DashboardModuleSetting(db.Model):
    """
    Represents a dashboard module configuration for a specific user.

    Each instance defines the type and position of a module in the user's dashboard layout.

    Attributes:
        id (int): Unique identifier for the dashboard module.
        user_id (int): ID of the user this module setting belongs to.
        module_type (str): Type or identifier of the module (e.g., "weather", "graph").
        position (int): Sort or layout order of the module (lower = higher priority).
    """
    __tablename__ = "dashboard_modules"

    id: db.Mapped[int] = db.Column(db.INTEGER, primary_key=True)
    user_id: db.Mapped[int] = db.Column(db.INTEGER, nullable=False)
    module_type: db.Mapped[str] = db.Column(db.VARCHAR(50), nullable=False)
    position: db.Mapped[int] = db.Column(db.INTEGER, nullable=False, default=0)
