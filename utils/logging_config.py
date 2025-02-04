import logging
import os

def setup_logging():
    """
    Configura o logging para o projeto.
    """
    # Cria a pasta de logs se não existir
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Configuração do logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),  # Logs em arquivo
            logging.StreamHandler()              # Logs no console
        ]
    )

    logging.info("Logging configurado com sucesso.")