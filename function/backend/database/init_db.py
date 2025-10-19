from .users import User, Role
from .settings import ManufacturerSetting, ManufacturerCategorySetting, LocationSetting
from extensions import db
import pandas as pd


MANUFACTURER_PATH = r'database/resources/manufacturer.csv'
CATEGORY_PATH = r'database/resources/category.csv'
LOCATION_PATH = r'database/resources/location.csv'


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
        df = pd.read_csv(MANUFACTURER_PATH, delimiter=',')
        df.fillna('', inplace=True)

        records = df.to_dict(orient='records')
        objects = [ManufacturerSetting(**record) for record in records]

        db.session.bulk_save_objects(objects)
        db.session.commit()
        print(f"✅ {len(objects)} Hersteller importiert.")
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")


def seed_category() -> None:
    """
    Create initial categories in database
    :return:
    """
    existing = ManufacturerCategorySetting.query.first()
    if existing:
        print("⚠️ Kategorien existieren bereits.")
        return

    try:
        df = pd.read_csv(CATEGORY_PATH, delimiter=',')
        df.fillna('', inplace=True)

        records = df.to_dict(orient='records')
        objects = [ManufacturerCategorySetting(**record) for record in records]

        db.session.bulk_save_objects(objects)
        db.session.commit()
        print(f"✅ {len(objects)} Kategorien importiert.")
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")


def seed_location() -> None:
    """
    Create initial locations in database
    :return:
    """
    existing = LocationSetting.query.first()
    if existing:
        print("⚠️ Standort existieren bereits.")
        return

    try:
        df = pd.read_csv(LOCATION_PATH, delimiter=',')
        df.fillna('', inplace=True)

        records = df.to_dict(orient='records')
        objects = [LocationSetting(**record) for record in records]

        db.session.bulk_save_objects(objects)
        db.session.commit()
        print(f"✅ {len(objects)} Standorte importiert.")
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")
