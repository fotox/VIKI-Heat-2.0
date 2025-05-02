from .users import User, Role
from extensions import db


def seed_roles():
    # Init admin role
    existing = Role.query.filter_by(role_name='admin').first()
    if existing:
        print("⚠️ Role 'admin' all ready exists.")
    else:
        admin = Role(
            id=1,
            role_name='admin'
        )
        db.session.add(admin)

    # Init user role
    existing = Role.query.filter_by(role_name='user').first()
    if existing:
        print("⚠️ Role 'user' all ready exists.")
    else:
        user = Role(
            id=2,
            role_name='user'
        )
        db.session.add(user)

    db.session.commit()
    print('✅ User roles added')


def seed_users():
    existing = User.query.filter_by(username='viki').first()
    if existing:
        print("⚠️ User 'viki' existiert bereits.")
    else:
        admin = User(
            id=1,
            username="viki",
            role="admin"
        )
        admin.set_password("viki")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin erstellt.")
