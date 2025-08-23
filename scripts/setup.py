import structlog

from scripts import setup_path
setup_path()

from app.db import init_db
from scripts.populate_admin import populate_admin
from scripts.populate_activities import populate_activities

logger = structlog.get_logger(__name__)

if __name__ == "__main__":
    logger.info("-------------Starting development setup-------------")
    logger.info("Initializing database...")
    init_db()
    populate_admin()
    populate_activities()
    logger.info("-------------Development setup completed successfully-------------")
