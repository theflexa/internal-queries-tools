import pytest
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtCore import Qt
from frontend.gui import QueryWindow
from controller.query_controller import QueryController

@pytest.fixture
def app(qapp, qtbot):
    """
    Fixture para inicializar a janela principal.
    """
    controller = QueryController(disable_queries=True)  # Desabilita queries reais
    window = QueryWindow(controller)
    qtbot.addWidget(window)  # Adiciona a janela ao qtbot
    return window

def test_initial_state(app):
    """
    Testa o estado inicial da interface.
    """
    # Verifica se o título da janela está correto
    assert app.windowTitle() == "Supabase Query Tool"

    # Verifica se o dropdown contém as queries esperadas
    expected_queries = ["Buscar Usuários por País", "Filtrar Pedidos por Data"]
    assert [app.query_combo.itemText(i) for i in range(app.query_combo.count())] == expected_queries

    # Verifica se o botão de execução está visível
    assert app.run_btn.isVisible()

def test_query_selection(app, qtbot):
    """
    Testa a seleção de uma query no dropdown.
    """
    # Seleciona a primeira query no dropdown
    app.query_combo.setCurrentIndex(0)
    assert app.query_combo.currentText() == "Buscar Usuários por País"

    # Verifica se os campos de parâmetros foram atualizados corretamente
    assert app.params_form.rowCount() == 1
    assert app.params_form.itemAt(0, QFormLayout.ItemRole.LabelRole).widget().text() == "country"

def test_execute_query(app, qtbot):
    """
    Testa a execução de uma query com dados simulados.
    """
    # Seleciona a query "Buscar Usuários por País"
    app.query_combo.setCurrentIndex(0)

    # Preenche o campo de parâmetro
    country_input = app.params_form.itemAt(0, QFormLayout.ItemRole.FieldRole).widget()
    country_input.setText("Brasil")

    # Clica no botão de execução
    qtbot.mouseClick(app.run_btn, Qt.MouseButton.LeftButton)

    # Verifica se a mensagem de sucesso foi exibida
    assert "Dados retornados: 1 registros." in app.statusBar().currentMessage()

def test_invalid_query(app, qtbot):
    """
    Testa o comportamento da interface em caso de erro.
    """
    # Seleciona a query "Filtrar Pedidos por Data"
    app.query_combo.setCurrentIndex(1)

    # Preenche os campos de parâmetro com valores inválidos
    start_date_input = app.params_form.itemAt(0, QFormLayout.ItemRole.FieldRole).widget()
    end_date_input = app.params_form.itemAt(1, QFormLayout.ItemRole.FieldRole).widget()
    start_date_input.setText("2023-01-01")
    end_date_input.setText("2023-12-31")

    # Simula um erro no controlador
    def mock_execute_query(query_name, params):
        raise ValueError("Erro simulado")

    app.controller.execute_query = mock_execute_query

    # Clica no botão de execução
    qtbot.mouseClick(app.run_btn, Qt.MouseButton.LeftButton)

    # Verifica se a mensagem de erro foi exibida
    assert "Erro simulado" in app.statusBar().currentMessage()