# frontend/styles.py

STYLE_SHEET = """
    /* Estilo geral da janela */
    QMainWindow {
        background-color: #F5F5F5;  /* Cinza claro */
        font-family: 'Segoe UI', sans-serif;
    }

    /* Container do cabeçalho (categoria + dropdown) */
    QWidget#query_header {
        margin-bottom: 15px;
    }

    /* Estilo do dropdown (QComboBox) */
    QComboBox {
        background-color: #FFFFFF;  /* Branco */
        border: 1px solid #CCCCCC;  /* Cinza médio */
        border-radius: 4px;
        padding: 5px;
        font-size: 14px;
        color: #333333;  /* Cinza escuro */
        min-width: 300px;
        height: 30px;  /* Altura fixa para alinhar com o label */
    }
    QComboBox:hover {
        border-color: #003641;  /* Azul Sicoob */
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #CCCCCC;  /* Cinza médio */
    }

    /* Estilo dos botões (QPushButton) */
    QPushButton {
        background-color: #003641;  /* Azul Sicoob */
        color: #FFFFFF;  /* Branco */
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: rgba(0, 54, 65, 0.8);  /* Azul Sicoob com transparência */
    }
    QPushButton:pressed {
        background-color: #00AE9D;  /* Verde Sicoob */
    }

    /* Estilo dos campos de entrada (QLineEdit) */
    QLineEdit {
        background-color: #FFFFFF;  /* Branco */
        border: 1px solid #CCCCCC;  /* Cinza médio */
        border-radius: 4px;
        padding: 5px;
        font-size: 14px;
        color: #333333;  /* Cinza escuro */
    }
    QLineEdit:focus {
        border-color: #003641;  /* Azul Sicoob */
    }

    /* Estilo dos rótulos (QLabel) */
    QLabel {
        font-size: 14px;
        color: #333333;  /* Cinza escuro */
    }

    /* Estilo do label de categoria de query */
    QLabel#query_type_label {
        font-size: 14px;
        font-weight: bold;
        padding: 4px;
        border-radius: 4px;
        color: white;
        min-width: 80px;  /* Largura mínima */
        height: 30px;  /* Altura fixa para alinhar com o dropdown */
        text-align: center;
    }

    /* Cores específicas para cada tipo de query */
    QLabel#query_type_label[query_type="SELECT"] {
        background-color: #00A859;  /* Verde Sicoob */
    }
    QLabel#query_type_label[query_type="DELETE"] {
        background-color: #E74C3C;  /* Vermelho */
    }
    QLabel#query_type_label[query_type="UPDATE"] {
        background-color: #FFD100;  /* Amarelo Sicoob */
    }
    QLabel#query_type_label[query_type="INSERT"] {
        background-color: #3498DB;  /* Azul claro */
    }
    QLabel#query_type_label[query_type="PATH"] {
        background-color: #9B59B6;  /* Roxo */
    }

    /* Estilo da barra de status */
    QStatusBar {
        background-color: #FFFFFF;  /* Branco */
        color: #333333;  /* Cinza escuro */
        font-size: 12px;
        border-top: 1px solid #CCCCCC;  /* Cinza médio */
    }
    
    /* Contêiner do formulário de parâmetros */
    QWidget#params_container {
        margin: 0;
        padding: 0;
    }

    /* Esconde completamente quando vazio */
    QWidget#params_container:disabled {
        height: 0;
        width: 0;
    }
    
    /* Visualizador de resultados */
    QTableWidget {
        background-color: #FFFFFF;
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        font-size: 14px;
        margin-top: 10px;
    }
    QTableWidget::item {
        padding: 5px;
    }
    QHeaderView::section {
        background-color: #003641;
        color: white;
        padding: 5px;
        border: none;
    }

    QTextEdit {
        background-color: #FFFFFF;
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        padding: 10px;
        font-size: 14px;
        margin-top: 10px;
    }
    
    /* Container do cabeçalho */
    QWidget#header_container {
        background-color: transparent;
        padding: 10px;
    }

    /* Estilo do botão de informação */
    QToolButton {
        background-color: rgba(0, 54, 65, 0.4);
        border: none;
        padding: 5px;
        border-radius: 15px;
    }
    
    QToolButton:hover {
        background-color: rgba(0, 54, 65, 0.2); /* Transparência suave */
        border-radius: 15px; /* Mantém consistência do círculo */
    }
    
    QToolButton:pressed {
        background-color: rgba(0, 54, 65, 0.6); /* Cor mais evidente ao pressionar */
    }

    
    /* Caixa de diálogo de informações */
    QMessageBox {
        background-color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
    }
    QMessageBox QLabel {
        font-size: 14px;
        color: #333333;
    }
    QMessageBox QPushButton {
        background-color: #003641;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 14px;
    }
    QMessageBox QPushButton:hover {
        background-color: rgba(0, 54, 65, 0.8);
    }
    QMessageBox QPushButton:pressed {
        background-color: #00AE9D;
    }
"""