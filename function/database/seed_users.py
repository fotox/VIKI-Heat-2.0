"""
Legt initialen Admin-User an.
"""
from function.backend.app import create_app
from function.backend.extensions import db
from backend.api.auth.user import User

app = create_app()

with app.app_context():
    admin = User(username="admin", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin erstellt.")
