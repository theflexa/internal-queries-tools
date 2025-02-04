import requests
from datetime import datetime, timedelta
from importlib.metadata import version
import os
import json

class AppInfo:
    def __init__(self):
        self.version = self.get_version()
        self.developer = "Flexa"
        self.contact = "the.flexa@outlook.com"
        self.repository = "https://api.github.com/repos/theflexa/internal-queries-tools/releases/latest"
        self.license = "MIT"
        self.release_date_file = "release_date.json"
        self.release_date = self.get_release_date()

    def get_version(self):
        """
        Obtém a versão do pacote usando importlib.metadata, sincronizada com as tags do Git.
        """
        try:
            return version("deepseek_query_tool")  # Nome do seu pacote
        except Exception as e:
            print(f"Erro ao obter a versão: {e}")
            return "Versão não encontrada"

    def get_release_date(self):
        """
        Verifica se a data da última release precisa ser atualizada.
        Se não, usa a data armazenada localmente.
        """
        if os.path.exists(self.release_date_file):
            with open(self.release_date_file, "r") as f:
                data = json.load(f)
                last_update = datetime.fromisoformat(data.get("last_update", datetime.now().isoformat()))
                # Se a data for mais de 7 dias atrás, atualiza a data
                if datetime.now() - last_update < timedelta(days=7):
                    return data.get("release_date")

        # Se não houver arquivo ou se a data precisar ser atualizada
        try:
            response = requests.get(self.repository)
            response.raise_for_status()  # Vai gerar um erro se a requisição falhar
            release_info = response.json()
            release_date = release_info["published_at"][:10]  # Data no formato YYYY-MM-DD

            # Armazena a data localmente e atualiza a data de último acesso
            with open(self.release_date_file, "w") as f:
                json.dump({"release_date": release_date, "last_update": datetime.now().isoformat()}, f)

            return release_date
        except requests.RequestException as e:
            print(f"Erro ao acessar a API do GitHub: {e}")
            return datetime.now().strftime("%d/%m/%Y")

    def get_info_html(self):
        """
        Retorna as informações da aplicação formatadas em HTML.
        """
        return f"""
            <b>Versão:</b> {self.version}<br>
            <b>Desenvolvido por:</b> {self.developer}<br>
            <b>Data da Versão:</b> {self.release_date}<br>
            <b>Contato:</b> {self.contact}<br>
            <b>Repositório:</b> <a href="{self.repository}">GitHub</a><br>
            <b>Licença:</b> {self.license}
        """
