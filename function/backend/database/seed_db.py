from .users import User, Role
from extensions import db


def seed_roles():
    existing = Role.query.filter_by(role_name='admin').first()
    if existing:
        print("⚠️ Rolle 'admin' existiert bereits.")
        return

    admin = Role(
        id=1,
        role_name='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print('✅ Admin role added')


def seed_users():
    existing = User.query.filter_by(username='viki').first()
    if existing:
        print("⚠️ User 'viki' existiert bereits.")
        return

    admin = User(
        id=1,
        username="viki",
        role="admin"
    )
    admin.set_password("viki")
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin erstellt.")
