# populate.py
import json
import structlog 

from app.db import get_session, init_db
from app.models import Activity

logger = structlog.get_logger(__name__)

init_db()

def populate_activities():
    with open("scripts/activities.json", "r") as f:
        items = json.load(f)

    with get_session() as session:
        for item in items:
            exists = session.query(Activity).filter(
                Activity.title == item['title'],
                Activity.category == item['category'],
            ).first()
            if not exists:
                logger.info(f"CREATE activity: {item['title']}")
                session.add(Activity(**item))
                session.commit()
            else:
                logger.warning(f"Activity already exists: {item['title']}")

if __name__ == "__main__":
    populate_activities()
    logger.info("Activities populated successfully.")