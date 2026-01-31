

import structlog
from dotenv import load_dotenv
from supabase import create_client, Client

from app import settings


supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)

logger = structlog.get_logger(__name__)


def get_online_db_table(table_name: str):
    """Fetch all records from a Supabase table."""
    try:
        logger.info(f"Fetching data from Supabase table: {table_name}")
        response = supabase.table(table_name).select("*").execute()
        logger.info(f"Fetched data from Supabase table: {table_name}", response=response)
        return response.data
    except Exception as e:
        logger.error(f"Exception occurred while fetching data from {table_name}: {str(e)}")
        return []



