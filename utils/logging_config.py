import logging
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime

def get_app_log_dir() -> Path:
    """
    Retorna o diretório de logs da aplicação baseado no sistema operacional.
    Tenta múltiplos locais em ordem de preferência.
    """
    try:
        # Primeira tentativa: %APPDATA% no Windows, ~/.deepseek-tool no Linux/Mac
        if sys.platform == 'win32':
            base_dir = os.path.join(os.environ.get('APPDATA', ''), 'DeepSeek-Tool')
        else:
            base_dir = os.path.join(os.path.expanduser('~'), '.deepseek-tool')
        
        log_dir = Path(base_dir) / 'logs'
        # Testa se podemos escrever no diretório
        log_dir.mkdir(parents=True, exist_ok=True)
        test_file = log_dir / '.test'
        test_file.touch()
        test_file.unlink()
        return log_dir
    except:
        try:
            # Segunda tentativa: Diretório do executável
            if getattr(sys, 'frozen', False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            
            log_dir = Path(base_dir) / 'logs'
            log_dir.mkdir(parents=True, exist_ok=True)
            test_file = log_dir / '.test'
            test_file.touch()
            test_file.unlink()
            return log_dir
        except:
            # Última tentativa: Diretório temporário do sistema
            temp_dir = Path(tempfile.gettempdir()) / 'DeepSeek-Tool' / 'logs'
            temp_dir.mkdir(parents=True, exist_ok=True)
            return temp_dir

def setup_logging():
    """
    Configura o logging para o projeto usando o diretório apropriado do sistema.
    """
    try:
        # Obtém o diretório de logs
        log_dir = get_app_log_dir()
        
        # Define o arquivo de log com timestamp para evitar conflitos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f'app_{timestamp}.log'
        
        # Configuração do formato do log
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)
        
        # Handler para arquivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Configura o logger root
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Remove handlers existentes para evitar duplicação
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Adiciona os novos handlers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        logging.info(f"Logging configurado com sucesso em: {log_file}")
        
    except Exception as e:
        # Em caso de erro, configura apenas o logging para console
        print(f"⚠️ Erro ao configurar logging em arquivo: {e}")
        print("ℹ️ Usando apenas logging no console")
        
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[logging.StreamHandler()]
        )