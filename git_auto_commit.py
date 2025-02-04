import os
import subprocess


def run_command(command: str) -> bool:
    """Executa comandos no terminal, capturando erros."""
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        print(f"❌ Erro ao executar: '{command}'")
        return False
    return True


def check_git_status() -> None:
    """Verifica se o repositório Git está configurado corretamente."""
    # Verifica se a pasta tem um repositório Git
    if not os.path.exists(".git"):
        print("⚠️ Este diretório não parece ser um repositório Git. Inicialize com `git init`.")
        exit(1)

    # Verifica o estado atual do repositório
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("⚠️ Nenhuma alteração para commitar. Certifique-se de editar os arquivos antes.")
        exit(1)


def main():
    check_git_status()

    # Solicitar o nome da branch (padrão: 'main')
    branch_name = input("Informe a branch (pressione Enter para 'main'): ") or "main"

    # Solicitar a descrição do commit
    commit_message = input("Descrição do commit: ").strip()
    if not commit_message:
        print("❌ A mensagem do commit não pode estar vazia.")
        exit(1)

    print("\n🚀 Automatizando Git...\n")

    # Executar comandos com validações
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


if __name__ == "__main__":
    try:
        # Verifica se Git está configurado corretamente
        subprocess.run("git --version", shell=True, check=True)
        main()
    except subprocess.CalledProcessError:
        print("❌ Git não está instalado ou configurado corretamente.")
        exit(1)
