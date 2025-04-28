"""
Legt initialen Admin-User an.
"""
from backend.api.auth.user import User
from backend.app import create_app
from backend.extensions import db

app = create_app()

with app.app_context():
    admin = User(username="admin", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin erstellt.")
