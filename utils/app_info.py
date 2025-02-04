# app_info.py
from datetime import datetime

class AppInfo:
    def __init__(self, version_file="version.txt"):
        self.version_file = version_file
        self.developer = "Sua Empresa"
        self.contact = "suporte@suaempresa.com"
        self.repository = "https://github.com/suaempresa/seuprojeto"
        self.license = "MIT"

    def get_version(self):
        """
        Lê a versão do arquivo version.txt.
        Se o arquivo não existir, retorna "Desenvolvimento Local".
        """
        try:
            with open(self.version_file, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return "Desenvolvimento Local"

    def get_release_date(self):
        """
        Retorna a data da última modificação do arquivo version.txt.
        Se o arquivo não existir, retorna a data atual.
        """
        try:
            timestamp = os.path.getmtime(self.version_file)
            return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")
        except FileNotFoundError:
            return datetime.now().strftime("%d/%m/%Y")

    def get_info_html(self):
        """
        Retorna as informações da aplicação formatadas em HTML.
        """
        version = self.get_version()
        release_date = self.get_release_date()

        return f"""
            <b>Versão:</b> {version}<br>
            <b>Desenvolvido por:</b> {self.developer}<br>
            <b>Data da Versão:</b> {release_date}<br>
            <b>Contato:</b> {self.contact}<br>
            <b>Repositório:</b> <a href="{self.repository}">GitHub</a><br>
            <b>Licença:</b> {self.license}
        """