import os
import subprocess

def run_command(command: str) -> None:
    """Executa comandos do shell e imprime a saída."""
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        print(f"Erro ao executar: {command}")
        exit(1)

def main():
    branch_name = input("Informe o nome da branch (ou pressione Enter para 'main'): ") or "main"
    commit_message = input("Descrição do commit: ").strip()
    if not commit_message:
        print("A mensagem do commit não pode estar vazia.")
        exit(1)

    print("\n🚀 Automatizando processo Git...\n")
    run_command("git add .")  # Adiciona todos os arquivos
    run_command(f'git commit -m "{commit_message}"')  # Realiza o commit
    run_command(f"git push origin {branch_name}")  # Envia para o repositório remoto

    print("\n✅ Commit enviado com sucesso!")

if __name__ == "__main__":
    # Verifica se Git está configurado
    try:
        subprocess.run("git --version", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Git não está instalado ou configurado.")
        exit(1)

    main()
