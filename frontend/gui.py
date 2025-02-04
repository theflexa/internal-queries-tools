import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QComboBox, QTableWidget,
    QPushButton, QLineEdit, QLabel, QFormLayout, QMessageBox,
    QHBoxLayout, QSpacerItem, QSizePolicy, QTableWidgetItem, QTextEdit
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QIcon
from frontend.styles import STYLE_SHEET

logger = logging.getLogger(__name__)

class QueryWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.queries = {
            "Remover Registro de Job": ["job_id"],
            "Buscar Jobs Recentes": []
        }
        self.initUI()

    def initUI(self):
        logger.info("Inicializando interface gráfica.")
        self.setWindowTitle("SNC Query Tool")
        self.setGeometry(100, 100, 800, 500)
        self.setWindowIcon(QIcon("assets/logo.ico"))
        self.setStyleSheet(STYLE_SHEET)  # Aplica o estilo CSS

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Container do cabeçalho (acima do logotipo)
        header_container = QWidget()
        header_container.setObjectName("header_container")  # Define o nome do container
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 30)
        header_layout.setSpacing(0)

        # Botão de informação no canto superior direito
        info_button = QToolButton()
        info_button.setIcon(QIcon("assets/info_icon.svg"))  # Substitua pelo caminho do ícone
        info_button.setToolTip("Informações da Aplicação")
        info_button.clicked.connect(self.show_app_info)
        info_button.setFixedSize(30, 30)  # Tamanho fixo para o botão

        # Adiciona o botão ao cabeçalho (alinhado à direita)
        header_layout.addStretch()  # Empurra o botão para a direita
        header_layout.addWidget(info_button)

        # Adiciona o cabeçalho ao layout principal
        layout.addWidget(header_container)

        # Logo
        logo = QLabel()
        logo.setPixmap(QPixmap("assets/logo.ico").scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

        # Container para categoria + dropdown
        query_header = QWidget()
        query_header_layout = QHBoxLayout(query_header)
        query_header_layout.setContentsMargins(0, 0, 0, 0)
        query_header_layout.setSpacing(5)  # Espaçamento entre o label e o dropdown

        # Formulário de parâmetros (agora dentro de um widget contêiner)
        self.params_container = QWidget()  # Novo contêiner
        self.params_form = QFormLayout(self.params_container)
        layout.addWidget(self.params_container)  # Adiciona o contêiner ao layout principal

        # Label da categoria (ex: SELECT, DELETE)
        self.query_type_label = QLabel("SELECT")
        self.query_type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.query_type_label.setFixedSize(80, 40)  # Tamanho fixo para uniformidade
        query_header_layout.addWidget(self.query_type_label)

        # Dropdown
        self.query_combo = QComboBox()
        self.query_combo.addItems(self.queries.keys())
        self.query_combo.currentTextChanged.connect(self.update_query_type)
        self.query_combo.currentTextChanged.connect(self.update_params)
        query_header_layout.addWidget(self.query_combo)

        layout.addWidget(query_header)

        # Formulário de parâmetros (agora dentro de um widget contêiner)
        self.params_container = QWidget()  # Novo contêiner
        self.params_form = QFormLayout(self.params_container)
        layout.addWidget(self.params_container)  # Adiciona o contêiner ao layout principal

        # Spacer para manter o espaço quando não há parâmetros
        self.params_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(self.params_spacer)

        # Botão de execução
        self.run_btn = QPushButton("Executar Query")
        self.run_btn.clicked.connect(self.execute_query)
        layout.addWidget(self.run_btn)

        # Visualizador de resultados
        self.result_viewer = QWidget()
        self.result_layout = QVBoxLayout(self.result_viewer)

        # Tabela para resultados SELECT
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(0)
        self.result_table.setRowCount(0)
        self.result_table.hide()

        # Área de texto para outras operações
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.hide()

        self.result_layout.addWidget(self.result_table)
        self.result_layout.addWidget(self.result_text)
        layout.addWidget(self.result_viewer)

        # Barra de status
        self.statusBar().showMessage("Pronto")

        self.update_params()
        self.update_query_type()  # Atualiza a cor inicial

    def update_query_type(self):
        """Atualiza a cor e o texto do label conforme o tipo de query."""
        current_query = self.query_combo.currentText()
        query_type = self._get_query_type(current_query)  # Obtém o tipo de query

        # Define a cor com base no tipo de query
        color_map = {
            "SELECT": "#00A859",  # Verde Sicoob
            "DELETE": "#E74C3C",  # Vermelho
            "UPDATE": "#FFD100",  # Amarelo Sicoob
            "INSERT": "#3498DB",  # Azul claro
            "PATH": "#9B59B6"     # Roxo
        }

        color = color_map.get(query_type, "#333333")  # Cinza como padrão
        self.query_type_label.setText(query_type)
        self.query_type_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                border-radius: 4px;
                padding: 4px;
                font-weight: bold;
            }}
        """)

    def _get_query_type(self, query_name):
        """
        Retorna o tipo de query com base no nome da query.
        """
        if "Buscar" in query_name:
            return "SELECT"
        elif "Remover" in query_name:
            return "DELETE"
        elif "Atualizar" in query_name:
            return "UPDATE"
        else:
            return "UNKNOWN"

    def update_params(self):
        """
        Atualiza o formulário de parâmetros com base na query selecionada.
        """
        current_query = self.query_combo.currentText()
        params = self.queries[current_query]

        # Limpa o formulário
        while self.params_form.rowCount() > 0:
            self.params_form.removeRow(0)

        # Adiciona campos se houver parâmetros
        self.inputs = {}
        if params:
            for param in params:
                self.inputs[param] = QLineEdit()
                self.params_form.addRow(QLabel(param), self.inputs[param])
            self.params_container.show()  # Mostra o contêiner
            self.params_spacer.changeSize(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)  # Desativa o spacer
        else:
            self.params_container.hide()  # Esconde o contêiner
            self.params_spacer.changeSize(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)  # Ativa o spacer

    def execute_query(self):
        """
        Executa a query selecionada e exibe os resultados.
        """
        query_name = self.query_combo.currentText()
        params = {key: input.text() for key, input in self.inputs.items()}

        try:
            result = self.controller.execute_query(query_name, params)

            # Esconde ambos os componentes primeiro
            self.result_table.hide()
            self.result_text.hide()

            if isinstance(result, dict) and "data" in result:
                data = result["data"]
                query_type = self._get_query_type(query_name)

                if query_type == "SELECT":
                    self._display_table_result(data)
                else:
                    self._display_text_result(
                        f"Operação {query_type} concluída com sucesso!\nRegistros afetados: {len(data)}")
            else:
                self._display_text_result("Formato de dados inválido retornado pelo controlador.")

        except Exception as e:
            logger.error(f"Erro na interface: {e}")
            self._display_text_result(f"Erro: {str(e)}")
            QMessageBox.critical(self, "Erro", str(e))

    def _display_table_result(self, data):
        """Exibe resultados tabulares."""
        if not data:
            self._display_text_result("Nenhum dado encontrado.")
            return

        # Configura a tabela
        self.result_table.clear()
        headers = list(data[0].keys())
        self.result_table.setColumnCount(len(headers))
        self.result_table.setRowCount(len(data))
        self.result_table.setHorizontalHeaderLabels(headers)

        # Preenche os dados
        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(headers):
                item = QTableWidgetItem(str(row_data.get(header, "")))
                self.result_table.setItem(row_idx, col_idx, item)

        self.result_table.resizeColumnsToContents()
        self.result_table.show()

    def _display_text_result(self, message):
        """Exibe mensagens de operações não-SELECT."""
        self.result_text.clear()
        self.result_text.setPlainText(message)
        self.result_text.show()

    def show_app_info(self):
        """
        Exibe uma caixa de diálogo com informações da aplicação.
        """
        app_info = """
            <b>Versão:</b> 1.0.0<br>
            <b>Desenvolvido por:</b> Sua Empresa<br>
            <b>Data da Versão:</b> 03/02/2024<br>
            <b>Contato:</b> suporte@suaempresa.com<br>
            <b>Repositório:</b> <a href="https://github.com/suaempresa/seuprojeto">GitHub</a><br>
            <b>Licença:</b> MIT
        """

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Informações da Aplicação")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setTextFormat(Qt.TextFormat.RichText)  # Permite HTML
        msg_box.setText(app_info)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()