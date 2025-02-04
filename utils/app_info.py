import os
import json


class AppInfo:
    def __init__(self):
        self.developer = "Flexa"
        self.contact = "the.flexa@outlook.com"
        # Caminho para o arquivo oculto contendo informações da versão
        self.cache_file = ".release_info.json"
        self.license = "MIT"
        # Obtém as informações de versão e data diretamente do arquivo oculto
        info = self.get_release_info()
        self.version = info.get("tag_name", "Versão não encontrada")
        self.release_date = info.get("published_at", "Não encontrado")

    def get_release_info(self) -> dict:
        """
        Retorna as informações de versão e data armazenadas localmente no arquivo .release_info.json.
        Caso o arquivo não exista ou esteja corrompido, retorna valores padrão.
        """
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    data = json.load(f)
                return data
            except Exception as e:
                print(f"Erro ao ler o cache: {e}")

        # Se o arquivo não existir ou estiver corrompido, retorna valores padrão
        print("⚠️ Arquivo de cache não encontrado ou corrompido. Informações padrão serão usadas.")
        return {"tag_name": "Versão não encontrada", "published_at": "Não encontrado"}

    def get_info_html(self) -> str:
        """
        Retorna as informações da aplicação formatadas em HTML.
        """
        return f"""
            <b>Versão:</b> {self.version}<br>
            <b>Desenvolvido por:</b> {self.developer}<br>
            <b>Data da Versão:</b> {self.release_date}<br>
            <b>Contato:</b> {self.contact}<br>
            <b>Repositório:</b> <a href="https://github.com/theflexa/internal-queries-tools">GitHub</a><br>
            <b>Licença:</b> {self.license}
        """


# Exemplo de uso:
if __name__ == "__main__":
    app_info = AppInfo()
    print(app_info.get_info_html())
