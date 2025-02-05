import os
from pathlib import Path
import json
from getpass import getpass

def load_existing_env():
    """Carrega configurações existentes do .env se existir"""
    env_data = {}
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    env_data[key] = value
    return env_data

def get_user_input(key, current_value=None):
    """Obtém input do usuário com valor atual como sugestão"""
    if current_value:
        value = input(f"Digite {key} (Enter para manter '{current_value}'): ").strip()
        return value if value else current_value
    else:
        while True:
            value = input(f"Digite {key}: ").strip()
            if value:
                return value
            print("⚠️ Este campo é obrigatório!")

def setup_env():
    """Configura o arquivo .env interativamente"""
    print("🔧 Configurando arquivo .env\n")
    
    # Carrega configurações existentes
    current_config = load_existing_env()
    
    # Configurações necessárias
    config = {
        "SUPABASE_URL": current_config.get("SUPABASE_URL", ""),
        "SUPABASE_KEY": current_config.get("SUPABASE_KEY", "")
    }
    
    print("Por favor, forneça as seguintes informações:")
    print("(Pressione Enter para manter os valores atuais, se existirem)\n")
    
    # Obtém valores do usuário
    for key in config:
        config[key] = get_user_input(key, config[key])
    
    # Salva o arquivo .env
    env_path = Path(__file__).parent.parent / ".env"
    with open(env_path, "w", encoding="utf-8") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    
    print("\n✨ Arquivo .env configurado com sucesso!")
    print(f"📁 Salvo em: {env_path}")

def main():
    try:
        setup_env()
    except KeyboardInterrupt:
        print("\n\n❌ Configuração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro ao configurar .env: {e}")

if __name__ == "__main__":
    main() 