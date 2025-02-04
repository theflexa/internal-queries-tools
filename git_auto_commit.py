import os
import subprocess
from utils.update_version import main as update_version_main


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


def get_version_from_git() -> str:
    """Obtém a versão mais recente a partir das tags do Git (ex: v1.0.1)."""
    try:
        result = subprocess.run("git describe --tags --abbrev=0", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()  # Retorna a tag mais recente
        else:
            print("⚠️ Não foi possível obter a versão do Git.")
            return "v0.0.0"  # Valor padrão se não houver tag
    except subprocess.CalledProcessError:
        return "v0.0.0"


def create_tag(version: str):
    """Cria uma nova tag no Git com base na versão extraída."""
    print(f"\n📑 Criando a tag '{version}'...")
    if not run_command(f"git tag {version}"):
        print("❌ Falha ao criar a tag.")
        exit(1)
    if not run_command(f"git push origin {version}"):
        print(f"❌ Falha ao fazer push da tag '{version}'.")
        exit(1)
    print(f"\n✅ Tag '{version}' criada e enviada com sucesso!")


def create_release(version: str):
    """Cria uma release no GitHub associada à tag."""
    print(f"\n📦 Criando a release para a tag '{version}'...")
    # Você pode usar a API do GitHub para criar a release automaticamente.
    # Exemplo simples de como poderia ser feito via `curl` (ou você pode usar o GitHub CLI)
    release_message = input("Mensagem da release: ")
    command = f"gh release create {version} --title '{version}' --notes '{release_message}'"
    if not run_command(command):
        print("❌ Falha ao criar a release no GitHub.")
        exit(1)
    print(f"\n✅ Release '{version}' criada com sucesso no GitHub!")


def main():
    check_git_status()

    # Incrementa versão antes do commit
    #print("\n🔄 Atualizando versão...")
    #update_version_main()

    # Solicita branch e commit message
    branch_name = input("Informe a branch (pressione Enter para 'main'): ") or "main"
    commit_message = input("Descrição do commit (ou pressione Enter para 'Atualiza versão'): ").strip() or "Atualiza versão automaticamente"

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

    # Obtém a versão do commit
    version = get_version_from_git()

    # Pergunta se o usuário deseja criar a tag ou release
    action_choice = input(f"\nDeseja criar a tag ou release com a versão '{version}'? (tag/release): ").strip().lower()
    if action_choice == "tag":
        # Cria uma tag com a versão do commit
        create_tag(version)
    elif action_choice == "release":
        # Cria uma tag e uma release associada
        create_tag(version)
        create_release(version)
    else:
        print("\n⚠️ Nenhuma tag ou release criada.")


if __name__ == "__main__":
    try:
        subprocess.run("git --version", shell=True, check=True)
        main()
    except subprocess.CalledProcessError:
        print("❌ Git não está instalado ou configurado corretamente.")
        exit(1)
