import os
import subprocess
import json
from datetime import datetime


def run_command(command: str) -> bool:
    """Executa comandos no terminal, capturando erros."""
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        print(f"❌ Erro ao executar: '{command}'")
        return False
    return True


def check_git_status() -> None:
    """Verifica se o repositório Git está configurado corretamente."""
    if not os.path.exists(".git"):
        print("⚠️ Este diretório não parece ser um repositório Git. Inicialize com `git init`.")
        exit(1)

    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("⚠️ Nenhuma alteração para commitar. Certifique-se de editar os arquivos antes.")
        exit(1)


def get_latest_tag() -> str:
    """Obtém a última tag do Git (ex: v1.0.1)."""
    try:
        result = subprocess.run("git describe --tags --abbrev=0", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()  # Retorna a última tag
        else:
            print("⚠️ Não foi possível obter a versão do Git.")
            return "v0.0.0"  # Valor padrão se não houver tag
    except subprocess.CalledProcessError:
        return "v0.0.0"


def increment_version(version: str) -> str:
    """Incrementa a versão seguindo o padrão 'vX.Y.Z'."""
    # Remove o prefixo "v" e divide em partes
    version_parts = version.lstrip("v").split(".")

    # Se a versão não estiver no formato esperado, retorna uma versão padrão
    if len(version_parts) != 3:
        return "v0.0.1"

    major, minor, patch = map(int, version_parts)

    # Incrementa o número de patch (pode ser ajustado para major ou minor conforme necessário)
    patch += 1

    # Retorna a nova versão formatada
    return f"v{major}.{minor}.{patch}"


def tag_exists(version: str) -> bool:
    """Verifica se a tag já existe no repositório."""
    result = subprocess.run(f"git tag -l {version}", shell=True, capture_output=True, text=True)
    return version in result.stdout.strip()


def create_tag(version: str):
    """Cria uma nova tag no Git com base na versão extraída, se a tag não existir."""
    if tag_exists(version):
        print(f"⚠️ A tag '{version}' já existe. Não será criada novamente.")
        return
    print(f"\n📑 Criando a tag '{version}'...")
    if not run_command(f"git tag {version}"):
        print("❌ Falha ao criar a tag.")
        exit(1)
    if not run_command(f"git push origin {version}"):
        print(f"❌ Falha ao fazer push da tag '{version}'.")
        exit(1)
    print(f"\n✅ Tag '{version}' criada e enviada com sucesso!")


def generate_release_info(version: str):
    """Gera e salva o arquivo .release_info.json com informações de versão e data."""
    release_info = {
        "tag_name": version,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    # Cria ou sobrescreve o arquivo .release_info.json
    with open(".release_info.json", "w") as f:
        json.dump(release_info, f, indent=4)
    print("\n✅ Arquivo '.release_info.json' atualizado!")


def main():
    check_git_status()

    # Obtém a última versão (tag)
    latest_version = get_latest_tag()

    # Incrementa a versão
    new_version = increment_version(latest_version)
    print(f"\n🔄 A nova versão será: {new_version}")

    # Gera e atualiza o arquivo .release_info.json
    generate_release_info(new_version)

    print(f"\nInformação: Quando uma Tag nova é criada, um CI/CD é acionado para gerar o executável desta versão.")
    print(f"Entretanto, também é possível gerar manualmente.")

    # Solicita branch e commit message
    branch_name = input("Informe a branch (pressione Enter para 'main'): ") or "main"
    commit_message = input(
        "Descrição do commit (ou pressione Enter para 'Atualiza versão'): ").strip() or "Atualiza versão automaticamente"

    print("\n🚀 Automatizando Git...\n")

    if not run_command("git add ."):
        print("❌ Falha ao adicionar arquivos.")
        exit(1)

    if not run_command(f'git commit -m "{commit_message}"'):
        print("⚠️ Nenhuma alteração para commitar.")
        exit(1)

    if not run_command(f"git push origin {branch_name}"):
        print(f"❌ Falha ao fazer push para a branch '{branch_name}'. Verifique se ela existe.")
        exit(1)

    print("\n✅ Commit enviado com sucesso!")

    # Pergunta se o usuário deseja criar a tag
    create_tag_choice = input(f"\nDeseja criar a tag com a versão '{new_version}'? (s/n): ").strip().lower()

    if create_tag_choice == "s":
        # Cria uma tag com a versão incrementada
        create_tag(new_version)
    else:
        print("\n⚠️ Nenhuma tag criada.")


if __name__ == "__main__":
    try:
        subprocess.run("git --version", shell=True, check=True)
        main()
    except subprocess.CalledProcessError:
        print("❌ Git não está instalado ou configurado corretamente.")
        exit(1)
