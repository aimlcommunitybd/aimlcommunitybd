# populate.py

from sqlmodel import select

from app.db import get_session, init_db
from app.models import Activity

import json
import structlog
from datetime import datetime

logger = structlog.get_logger(__name__)


def populate_activities():
    with open("scripts/activities.json", "r") as f:
        items = json.load(f)

    with get_session() as session:
        for item in items:
            exists = session.exec(
                select(Activity).where(
                    Activity.title == item["title"],
                    Activity.category == item["category"],
                )
            ).first()
            if not exists:
                logger.info(f"CREATE activity: {item['title']}")
                if 'event_date' in item and item['event_date']:
                    item['event_date'] = datetime.fromisoformat(item['event_date'])
                
                session.add(Activity(**item))
                session.commit()
            else:
                logger.warning(f"Activity already exists: {item['title']}")


if __name__ == "__main__":
    init_db()
    populate_activities()
    logger.info("Activities populated successfully.")
