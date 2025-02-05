import os
import subprocess
import json
from pathlib import Path
import shutil
import sys

# Ajusta o path para acessar o projeto principal
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def check_inno_setup():
    """Verifica se o Inno Setup está instalado"""
    inno_paths = [
        # Caminhos padrão de instalação
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        # Versões mais recentes
        r"C:\Program Files (x86)\Inno Setup 7\ISCC.exe",
        r"C:\Program Files\Inno Setup 7\ISCC.exe",
        # Caminhos alternativos comuns
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Inno Setup 6\ISCC.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\Inno Setup 6\ISCC.exe")
    ]
    
    for path in inno_paths:
        if os.path.exists(path):
            # Verifica se temos permissão de execução
            try:
                if os.access(path, os.X_OK):
                    return path
                else:
                    print(f"⚠️ Encontrado Inno Setup em {path}, mas sem permissão de execução")
            except Exception as e:
                print(f"⚠️ Erro ao verificar permissões de {path}: {e}")
                continue
    
    print("❌ Inno Setup não encontrado nos caminhos padrão")
    print("Por favor, instale o Inno Setup 6 ou 7:")
    print("https://jrsoftware.org/isdl.php")
    return None

def create_license():
    """Cria um arquivo de licença básico se não existir"""
    license_path = project_root / "LICENSE.txt"
    if not license_path.exists():
        with open(license_path, "w", encoding="utf-8") as f:
            f.write("""MIT License

Copyright (c) 2024 Flexa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""")
        print("✓ Arquivo LICENSE.txt criado")

def get_version():
    """Obtém a versão atual do arquivo .release_info.json"""
    try:
        release_file = project_root / ".release_info.json"
        if release_file.exists():
            with open(release_file) as f:
                data = json.load(f)
                return data.get("tag_name", "v0.0.1")
    except Exception as e:
        print(f"⚠️ Erro ao ler versão: {e}")
    return "v0.0.1"

def update_version_in_script(version):
    """Atualiza a versão no script do Inno Setup"""
    script_path = Path(__file__).parent / "installer_script.iss"
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Atualiza a versão e o nome do executável
    content = content.replace(
        '#define MyAppVersion "0.0.12"',
        f'#define MyAppVersion "{version.lstrip("v")}"'
    )
    content = content.replace(
        'Source: "..\\..\\dist\\DeepSeek-Tool.exe"',
        f'Source: "..\\..\\dist\\DeepSeek-Tool-{version}.exe"'
    )
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✓ Versão atualizada para {version}")

def check_required_files(version):
    """Verifica se todos os arquivos necessários existem"""
    files_to_check = {
        'executável': project_root / "dist" / f"DeepSeek-Tool-{version}.exe",
        'configuração': project_root / ".env",
        'pasta assets': project_root / "assets"
    }
    
    missing_files = []
    for name, path in files_to_check.items():
        if not path.exists():
            missing_files.append(f"- {name}: {path}")
    
    if missing_files:
        print("❌ Arquivos necessários não encontrados:")
        for file in missing_files:
            print(f"   {file}")
        return False
    
    return True

def check_and_setup_env():
    """Verifica e sugere configuração do .env se necessário"""
    env_path = project_root / ".env"
    if not env_path.exists():
        print("\n⚠️ Arquivo .env não encontrado!")
        setup_env = input("Deseja configurar o .env agora? (s/n): ").strip().lower()
        if setup_env == 's':
            setup_script = project_root / "build_tools" / "setup_env.py"
            if setup_script.exists():
                subprocess.run([sys.executable, str(setup_script)])
                return True
            else:
                print("❌ Script de configuração não encontrado!")
                return False
        return False
    return True

def main():
    print("🚀 Iniciando criação do instalador...\n")
    
    # Obtém e atualiza a versão
    version = get_version()
    print(f"   ℹ️ Versão detectada: {version}")
    update_version_in_script(version)
    
    # Verifica se o Inno Setup está instalado
    inno_path = check_inno_setup()
    if not inno_path:
        print("❌ Inno Setup não encontrado!")
        print("Por favor, instale o Inno Setup 6:")
        print("https://jrsoftware.org/isdl.php")
        return
    
    # Verifica e configura .env se necessário
    if not check_and_setup_env():
        print("\n❌ Build interrompido: arquivo .env necessário.")
        return
    
    # Verifica arquivos necessários
    if not check_required_files(version):
        print("\n❌ Build interrompido devido a arquivos faltantes.")
        return
    
    # Cria pasta para o instalador
    installer_dir = project_root / "installer"
    installer_dir.mkdir(exist_ok=True)
    
    # Cria arquivo de licença se não existir
    create_license()
    
    # Executa o Inno Setup
    print("🔨 Gerando instalador...")
    script_path = Path(__file__).parent / "installer_script.iss"
    result = subprocess.run([inno_path, str(script_path)], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✨ Instalador gerado com sucesso!")
        print("📁 O instalador está disponível na pasta installer/")
    else:
        print("\n❌ Erro ao gerar instalador:")
        print(result.stderr)

if __name__ == "__main__":
    main() 