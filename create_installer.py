import os
import subprocess
import json
from pathlib import Path
import shutil
import sys

def check_inno_setup():
    """Verifica se o Inno Setup está instalado"""
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe"
    ]
    
    for path in inno_paths:
        if os.path.exists(path):
            return path
    
    return None

def create_license():
    """Cria um arquivo de licença básico se não existir"""
    if not os.path.exists("LICENSE.txt"):
        with open("LICENSE.txt", "w", encoding="utf-8") as f:
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

def main():
    print("🚀 Iniciando criação do instalador...\n")
    
    # Verifica se o Inno Setup está instalado
    inno_path = check_inno_setup()
    if not inno_path:
        print("❌ Inno Setup não encontrado!")
        print("Por favor, instale o Inno Setup 6:")
        print("https://jrsoftware.org/isdl.php")
        return
    
    # Verifica se o executável existe
    if not any(Path("dist").glob("*.exe")):
        print("❌ Executável não encontrado na pasta dist/")
        print("Execute primeiro o build_exe.py para gerar o executável")
        return
    
    # Cria pasta para o instalador
    os.makedirs("installer", exist_ok=True)
    
    # Cria arquivo de licença se não existir
    create_license()
    
    # Executa o Inno Setup
    print("🔨 Gerando instalador...")
    result = subprocess.run([inno_path, "installer_script.iss"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✨ Instalador gerado com sucesso!")
        print("📁 O instalador está disponível na pasta installer/")
    else:
        print("\n❌ Erro ao gerar instalador:")
        print(result.stderr)

if __name__ == "__main__":
    main() 