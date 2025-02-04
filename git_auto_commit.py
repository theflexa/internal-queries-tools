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


def create_tag():
    """Cria uma nova tag no Git."""
    tag_name = input("Deseja criar uma nova tag? (S para sim, qualquer outra tecla para não): ").strip().lower()
    if tag_name == "s":
        tag_version = input("Informe o nome da nova tag (ex: v1.0.1): ").strip()
        if tag_version:
            print(f"\n📑 Criando a tag '{tag_version}'...")
            if not run_command(f"git tag {tag_version}"):
                print("❌ Falha ao criar a tag.")
                exit(1)
            if not run_command(f"git push origin {tag_version}"):
                print(f"❌ Falha ao fazer push da tag '{tag_version}'.")
                exit(1)
            print(f"\n✅ Tag '{tag_version}' criada e enviada com sucesso!")
        else:
            print("⚠️ Nome da tag inválido.")
            exit(1)


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

    # Pergunta ao usuário se deseja criar uma tag
    create_tag()


if __name__ == "__main__":
    try:
        subprocess.run("git --version", shell=True, check=True)
        main()
    except subprocess.CalledProcessError:
        print("❌ Git não está instalado ou configurado corretamente.")
        exit(1)
