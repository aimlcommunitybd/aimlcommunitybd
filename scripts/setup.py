from app.db import get_session, init_db
from app.models import User

init_db()


def populate_admin():
    with get_session() as session:
        user = User(email="admin@community.com")
        user.set_password("secret")
        user.is_admin = True
        user.active = True
        session.add(user)
        session.commit()
        print(f"Admin user: {user} created with email: {user.email}")


if __name__ == "__main__":
    populate_admin()
    print("Admin user created")
