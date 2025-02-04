import logging
from backend.database import SupabaseManager

logger = logging.getLogger(__name__)

class QueryController:
    def __init__(self, disable_queries=False):
        self.disable_queries = disable_queries
        if not self.disable_queries:
            self.supabase = SupabaseManager()

    def execute_query(self, query_name: str, params: dict):
        """
        Executa uma query no banco de dados ou retorna dados simulados.

        Args:
            query_name (str): Nome da query a ser executada.
            params (dict): Parâmetros necessários para a query.

        Returns:
            dict: Um dicionário contendo a chave "data" com os resultados da query.
        """
        try:
            logger.info(f"Executando query: {query_name} com parâmetros: {params}")

            if self.disable_queries:
                logger.info("Modo simulação ativado")
                return self._simulate_query(query_name, params)

            # Implementação real das queries
            if query_name == "Buscar Jobs Recentes":
                return self.supabase.execute_query("jobs", {"limit": 10})

            elif query_name == "Remover Registro de Job":
                return self.supabase.delete("jobs", {"job_id": params["job_id"]})

            else:
                raise ValueError("Query não implementada")

        except Exception as e:
            logger.error(f"Erro ao executar query: {str(e)}")
            return {"data": [], "erro": str(e)}

    def _simulate_query(self, query_name: str, params: dict):
        """
        Simula a execução de uma query, retornando dados fictícios.

        Args:
            query_name (str): Nome da query simulada.
            params (dict): Parâmetros necessários para a query.

        Returns:
            dict: Resultados simulados no formato {"data": [...]}
        """
        try:
            if query_name == "Buscar Jobs Recentes":
                # Simulação de SELECT
                simulated_data = [
                    {
                        "job_id": 1001,
                        "nome": "Backup Diário",
                        "status": "Concluído",
                        "data_execucao": "2024-02-01 03:00:00"
                    },
                    {
                        "job_id": 1002,
                        "nome": "Relatório de Vendas",
                        "status": "Falha",
                        "data_execucao": "2024-02-01 05:30:00"
                    },
                    {
                        "job_id": 1003,
                        "nome": "Sincronização de Dados",
                        "status": "Em Progresso",
                        "data_execucao": "2024-02-01 08:15:00"
                    }
                ]
                return {"data": simulated_data}

            elif query_name == "Remover Registro de Job":
                # Simulação de DELETE
                return {
                    "data": [
                        {
                            "operacao": "DELETE",
                            "job_id": params["job_id"],
                            "registros_afetados": 1,
                            "mensagem": "Registro removido com sucesso"
                        }
                    ]
                }

            else:
                raise ValueError(f"Query não implementada: {query_name}")

        except Exception as e:
            logger.error(f"Erro na simulação: {e}")
            return {"data": [], "erro": str(e)}