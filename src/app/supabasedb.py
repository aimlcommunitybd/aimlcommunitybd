# Supabase Flask Doc: https://supabase.com/docs/guides/getting-started/quickstarts/flask

import structlog
from dotenv import load_dotenv
from supabase import create_client, Client

from app import settings


supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)

logger = structlog.get_logger(__name__)


def get_online_db_table(table_name: str, order_by: str=None, desc: bool=True):
    """Fetch all records from a Supabase table.
    
    Args:
        table_name (str): Name of the Supabase table to fetch data from.
        order_by (str, optional): Column name to order the results by. Defaults to None.
        desc (bool, optional): Whether to order in descending order. Defaults to True.
    """
    try:
        logger.info(f"Fetching data from Supabase table: {table_name}")
        query = supabase.table(table_name).select("*")
        if order_by:
            query = query.order(order_by, desc=desc)
        response = query.execute()
        logger.info(f"Fetched data from Supabase table: {table_name}", response=response)
        return response.data
    except Exception as e:
        logger.error(f"Exception occurred while fetching data from {table_name}: {str(e)}")
        return []



