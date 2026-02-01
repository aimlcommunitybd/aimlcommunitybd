# Supabase Flask Doc: https://supabase.com/docs/guides/getting-started/quickstarts/flask

import structlog
from dotenv import load_dotenv
from supabase import create_client, Client

from app import settings
from app.utils import get_rows_from_csv

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
        logger.info(f"[Supabase] Fetching data: {table_name}")
        query = supabase.table(table_name).select("*")
        if order_by:
            query = query.order(order_by, desc=desc)
        response = query.execute()
        logger.info(f"[Supabase] Fetched data: {table_name}", response=response)
        return response.data
    except Exception as e:
        logger.error(f"[Supabase Exception] Table: {table_name} - Exc: {str(e)}")
        local_data = get_local_csv_data(table_name)
        return local_data


# FIXME: This is a temp solution. We should populate dev db during setup instead.
def get_local_csv_data(table_name:str):
    if settings.PRODUCTION:
        return []
    try:
        logger.warning(f"[Local Data] Fetching from CSV: {table_name}")
        return  get_rows_from_csv(f".data/{table_name}.csv")
    except Exception as csv_exc:
        logger.error(f"[Local Data Exception] Table: {table_name} - Exc: {str(csv_exc)}")
        return []


