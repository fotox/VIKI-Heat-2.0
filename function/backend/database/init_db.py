from .users import User, Role
from .settings import ManufacturerSetting
from extensions import db
import pandas as pd


CSV_PATH = r'database/resources/manufacturer.csv'


def seed_roles() -> None:
    """
    Create initial roles in database
    :return: None
    """
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
        print('✅ Admin role added')

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
        print('✅ User role added')

    db.session.commit()


def seed_users() -> None:
    """
    Create initial users in database
    :return: None
    """
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


def seed_manufacturers() -> None:
    """
    Create initial manufacturers in database
    :return:
    """
    existing = ManufacturerSetting.query.first()
    if existing:
        print("⚠️ Herstellerdaten existieren bereits.")
        return

    try:
        df = pd.read_csv(CSV_PATH, delimiter=';')
        df.fillna('', inplace=True)

        records = df.to_dict(orient='records')
        objects = [ManufacturerSetting(**record) for record in records]

        db.session.bulk_save_objects(objects)
        db.session.commit()
        print(f"✅ {len(objects)} Hersteller importiert.")
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")
