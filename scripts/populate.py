# populate.py
import json
from app.db import get_session, init_db
from app.models import Activity

init_db()

def populate_activities():
    with open("scripts/activities.json", "r") as f:
        items = json.load(f)

    with get_session() as session:
        for item in items:
            session.add(Activity(**item))
        session.commit()

if __name__ == "__main__":
    populate_activities()
    print("Activities populated successfully.")