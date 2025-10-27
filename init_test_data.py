from src.database import SessionLocal
from src.buildings.models import Building
from src.activities.models import Activity
from src.organizations.models import Organization, Phone


def init_data():
    db = SessionLocal()
    try:
        b1 = Building(
            address="г. Москва, ул. Ленина 1, офис 3",
            latitude=55.7522,
            longitude=37.6156,
        )
        b2 = Building(
            address="г. Москва, ул. Блюхера 32/1",
            latitude=55.7601,
            longitude=37.6209,
        )

        db.add_all([b1, b2])
        db.flush()

        food = Activity(name="Еда")
        meat = Activity(name="Мясная продукция", parent=food)
        milk = Activity(name="Молочная продукция", parent=food)

        cars = Activity(name="Автомобили")
        trucks = Activity(name="Грузовые", parent=cars)
        light = Activity(name="Легковые", parent=cars)
        parts = Activity(name="Запчасти", parent=light)
        accessories = Activity(name="Аксессуары", parent=light)

        db.add_all([food, meat, milk, cars, trucks, light, parts, accessories])
        db.flush()

        org1 = Organization(
            name="ООО Рога и Копыта",
            building_id=b2.id,
        )
        org1.activities.extend([meat, milk])

        org2 = Organization(
            name="ООО АвтоМир",
            building_id=b1.id,
        )
        org2.activities.extend([light, accessories, parts])

        db.add_all([org1, org2])
        db.flush()

        phones = [
            Phone(number="2-222-222", organization_id=org1.id),
            Phone(number="3-333-333", organization_id=org1.id),
            Phone(number="8-923-666-13-13", organization_id=org1.id),
            Phone(number="8-800-555-35-35", organization_id=org2.id),
        ]
        db.add_all(phones)

        db.commit()
        print("Test data successfully initialized.")

    except Exception as e:
        db.rollback()
        print("Error initializing test data:", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_data()
