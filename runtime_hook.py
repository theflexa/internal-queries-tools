
import os
import sys
import tempfile
from pathlib import Path

def ensure_app_directories():
    try:
        # Lista de diretórios para tentar criar/acessar
        dirs_to_check = []
        
        # Diretório %APPDATA%
        if os.name == 'nt':  # Windows
            appdata = os.environ.get('APPDATA', '')
            if appdata:
                dirs_to_check.append(Path(appdata) / 'DeepSeek-Tool' / 'logs')
        
        # Diretório do executável
        if getattr(sys, 'frozen', False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).parent
        dirs_to_check.append(base_dir / 'logs')
        
        # Diretório temporário
        dirs_to_check.append(Path(tempfile.gettempdir()) / 'DeepSeek-Tool' / 'logs')
        
        # Tenta criar e verificar acesso a cada diretório
        for dir_path in dirs_to_check:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                test_file = dir_path / '.test'
                test_file.touch()
                test_file.unlink()
            except:
                continue
                
        # Garante que o arquivo .env está disponível
        if getattr(sys, 'frozen', False):
            env_path = os.path.join(os.path.dirname(sys.executable), '.env')
            if not os.path.exists(env_path):
                # Cria um .env vazio se não existir
                open(env_path, 'a').close()
    except:
        pass  # Ignora erros, logging irá lidar com fallbacks

ensure_app_directories()
