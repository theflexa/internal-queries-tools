import re
import os

VERSION_FILE = "version.txt"

def read_version():
    """Lê a versão atual do arquivo version.txt."""
    if not os.path.exists(VERSION_FILE):
        return "0.0.0"
    with open(VERSION_FILE, "r") as file:
        return file.read().strip()

def validate_version_format(version: str) -> bool:
    """Valida se a versão segue o formato SemVer (ex: 1.2.3)."""
    return bool(re.match(r'^\d+\.\d+\.\d+$', version))

def increment_version(version):
    """Incrementa o PATCH da versão."""
    if not validate_version_format(version):
        print(f"⚠️ Versão inválida: '{version}'. Resetando para 0.0.1.")
        return "0.0.1"
    major, minor, patch = map(int, version.split("."))
    patch += 1
    return f"{major}.{minor}.{patch}"

def update_version_file(new_version):
    """Atualiza o arquivo version.txt."""
    with open(VERSION_FILE, "w") as file:
        file.write(new_version)
    print(f"🔄 Nova versão: {new_version}")

def main():
    current_version = read_version()
    new_version = increment_version(current_version)
    update_version_file(new_version)

if __name__ == "__main__":
    main()
