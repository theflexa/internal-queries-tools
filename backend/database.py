import logging
from supabase import create_client, Client
import os

logger = logging.getLogger(__name__)

class SupabaseManager:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.url, self.key)

    def execute_query(self, table: str, filters: dict):
        try:
            query = self.client.table(table).select("*")
            for key, value in filters.items():
                query = query.eq(key, value)
            logger.info(f"Executando query na tabela {table} com filtros {filters}")
            return query.execute()
        except Exception as e:
            logger.error(f"Erro ao executar query: {e}")
            raise