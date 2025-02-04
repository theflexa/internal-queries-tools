# app_info.py
APP_VERSION = "1.0.0"
DEVELOPED_BY = "Sua Empresa"
RELEASE_DATE = "03/02/2024"
CONTACT_EMAIL = "suporte@suaempresa.com"
REPOSITORY_URL = "https://github.com/suaempresa/seuprojeto"
LICENSE_TYPE = "MIT"

def get_app_info_html():
    return f"""
    <b>Versão:</b> {APP_VERSION}<br>
    <b>Desenvolvido por:</b> {DEVELOPED_BY}<br>
    <b>Data da Versão:</b> {RELEASE_DATE}<br>
    <b>Contato:</b> {CONTACT_EMAIL}<br>
    <b>Repositório:</b> <a href="{REPOSITORY_URL}">GitHub</a><br>
    <b>Licença:</b> {LICENSE_TYPE}
    """

