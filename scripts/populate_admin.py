from app.db import get_session, init_db
from app.models import User
from app import settings

import structlog
logger = structlog.get_logger(__name__)

def populate_admin():
    with get_session() as session:
        user = User(email=settings.ADMIN_EMAIL)
        user.set_password(settings.ADMIN_PASSWORD)
        user.is_admin = True
        user.active = True
        session.add(user)
        session.commit()
        logger.info(f"Admin user: {user} created with email: {user.email}")


if __name__ == "__main__":
    init_db()
    populate_admin()
