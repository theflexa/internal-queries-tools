import os
import sys
import shutil
import subprocess
from pathlib import Path

# Ajusta o path para acessar o projeto principal
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

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
    """Gera o executável com as configurações corporativas"""
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
        
        # Lê a versão atual
        version = "v0.0.1"  # versão padrão
        release_file = project_root / ".release_info.json"
        if release_file.exists():
            try:
                import json
                with open(release_file) as f:
                    data = json.load(f)
                    version = data.get("tag_name", version)
                print(f"   ✓ Versão encontrada: {version}")
            except Exception as e:
                print(f"   ⚠️ Erro ao ler versão: {e}. Usando versão padrão: {version}")
        
        # Comando PyInstaller com manifesto
        cmd = [
            python_path, "-m", "PyInstaller",
            "--onefile",
            "--clean",
            "--add-data", "assets/*;assets/",
            "--add-data", ".env;.",
            "--manifest", "app.manifest",  # Adiciona o manifesto
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
        
        print("   🔄 Executando PyInstaller...")
        print(f"   ℹ️ Comando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✓ Executável gerado com sucesso!")
            return True
        else:
            print("   ❌ Erro ao gerar executável:")
            print(result.stderr)
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