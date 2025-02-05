import os
import shutil
import subprocess
from pathlib import Path
import sys

def clean_builds():
    """Limpa builds anteriores"""
    try:
        print("🧹 Limpando builds anteriores...")
        for path in ['build', 'dist']:
            try:
                if os.path.exists(path):
                    shutil.rmtree(path)
                    print(f"   ✓ Pasta {path} removida")
                else:
                    print(f"   ℹ️ Pasta {path} não existe")
            except PermissionError as e:
                print(f"   ❌ Erro de permissão ao remover {path}: {e}")
                return False
            except Exception as e:
                print(f"   ❌ Erro ao remover {path}: {e}")
                return False
        return True
    except Exception as e:
        print(f"   ❌ Erro inesperado: {e}")
        return False

def build_executable():
    """Gera o executável com as mesmas configurações do workflow"""
    try:
        print("\n🔨 Gerando executável...")
        
        # Verifica se estamos em um ambiente virtual
        in_venv = sys.prefix != sys.base_prefix
        if not in_venv:
            print("   ⚠️ Não está em um ambiente virtual! Ativando venv...")
            if os.path.exists("venv/Scripts/python.exe"):
                python_path = os.path.abspath("venv/Scripts/python.exe")
            else:
                print("   ❌ Ambiente virtual não encontrado. Por favor, crie um com 'python -m venv venv'")
                return False
        else:
            python_path = sys.executable
        
        print(f"   ✓ Usando Python em: {python_path}")
        
        # Instala ou atualiza o PyInstaller e dependências
        print("   🔄 Verificando dependências...")
        for package in ["pyinstaller", "pyqt6", "python-dotenv"]:
            pip_cmd = [python_path, "-m", "pip", "install", "--upgrade", package]
            pip_result = subprocess.run(pip_cmd, capture_output=True, text=True)
            if pip_result.returncode != 0:
                print(f"   ❌ Erro ao instalar {package}: {pip_result.stderr}")
                return False
            print(f"   ✓ {package} instalado/atualizado")
        
        # Lê a versão atual do arquivo .release_info.json se existir
        version = "v0.0.1"  # versão padrão
        release_file = Path(".release_info.json")
        if release_file.exists():
            try:
                import json
                with open(release_file) as f:
                    data = json.load(f)
                    version = data.get("tag_name", version)
                print(f"   ✓ Versão encontrada: {version}")
            except Exception as e:
                print(f"   ⚠️ Erro ao ler versão: {e}. Usando versão padrão: {version}")
        else:
            print(f"   ℹ️ Arquivo de versão não encontrado. Usando versão padrão: {version}")
        
        # Verifica recursos necessários
        required_assets = ["logo.ico", "info_icon.svg"]
        missing_assets = []
        for asset in required_assets:
            if not (Path("assets") / asset).exists():
                missing_assets.append(asset)
        
        if missing_assets:
            print("   ❌ Arquivos necessários não encontrados:")
            for asset in missing_assets:
                print(f"      - assets/{asset}")
            return False
        
        # Comando PyInstaller usando o Python do ambiente virtual
        cmd = [
            python_path, "-m", "PyInstaller",
            "--onefile",
            "--clean",
            "--add-data", "assets/*;assets/",
            "--add-data", ".env;.",  # Inclui arquivo de configuração
            "--noupx",
            "--name", f"DeepSeek-Tool-{version}",
            "--noconfirm",
            "--hidden-import", "PyQt6.sip",
            "--hidden-import", "PyQt6.QtCore",
            "--hidden-import", "PyQt6.QtWidgets",
            "--hidden-import", "PyQt6.QtGui",
            "--hidden-import", "dotenv",
            "--hidden-import", "supabase",
            "--hidden-import", "requests",
            "--collect-data", "PyQt6",
            "--icon", "assets/logo.ico",
            "--runtime-hook", "runtime_hook.py",
            "main.py"
        ]
        
        # Cria o runtime hook para garantir acesso aos diretórios e configurações
        with open("runtime_hook.py", "w", encoding='utf-8') as f:
            f.write("""
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
""")
        
        print("   🔄 Executando PyInstaller...")
        print(f"   ℹ️ Comando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✓ Executável gerado com sucesso!")
            return True
        else:
            print("   ❌ Erro ao gerar executável:")
            print(result.stderr)
            if "PermissionError" in result.stderr:
                print("\n   💡 Dica: Tente executar o script como administrador")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro inesperado durante o build: {e}")
        import traceback
        print(f"   📑 Detalhes do erro:\n{traceback.format_exc()}")
        return False

def adjust_permissions():
    """Ajusta as permissões do executável"""
    print("\n🔒 Ajustando permissões...")
    
    # Lista todos os arquivos .exe na pasta dist
    exe_files = list(Path("dist").glob("*.exe"))
    
    if not exe_files:
        print("   ❌ Nenhum executável encontrado na pasta dist/")
        return False
    
    for exe_path in exe_files:
        try:
            # No Windows, tenta desbloquear o arquivo
            if os.name == 'nt':
                subprocess.run(["powershell", "-Command", f"Unblock-File -Path '{exe_path}'"])
                subprocess.run(["icacls", str(exe_path), "/grant", "Everyone:F"])
                print(f"   ✓ Permissões ajustadas para: {exe_path}")
        except Exception as e:
            print(f"   ❌ Erro ao ajustar permissões: {e}")
            return False
    
    return True

def main():
    print("🚀 Iniciando processo de build...\n")
    
    steps = [
        clean_builds,
        build_executable,
        adjust_permissions
    ]
    
    for step in steps:
        if not step():
            print("\n❌ Build interrompido devido a erros.")
            return
    
    print("\n✨ Build concluído com sucesso!")
    print("📁 O executável está disponível na pasta dist/")

if __name__ == "__main__":
    main() 