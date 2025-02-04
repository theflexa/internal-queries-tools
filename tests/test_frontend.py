import pytest
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtCore import Qt
from frontend.gui import QueryWindow
from controller.query_controller import QueryController


@pytest.fixture(scope="module")
def controller():
    return QueryController(disable_queries=True)


@pytest.fixture
def window(controller, qtbot):
    window = QueryWindow(controller)
    qtbot.addWidget(window)
    return window


def test_initial_state(window):
    assert window.windowTitle() == "Supabase Query Tool"
    expected_queries = ["Buscar Usuários por País", "Filtrar Pedidos por Data"]
    assert [window.query_combo.itemText(i) for i in range(window.query_combo.count())] == expected_queries
    assert window.run_btn.isVisible()


def test_query_selection(window, qtbot):
    window.query_combo.setCurrentIndex(0)
    assert window.query_combo.currentText() == "Buscar Usuários por País"
    assert window.params_form.rowCount() == 1
    label = window.params_form.itemAt(0, QFormLayout.ItemRole.LabelRole).widget().text()
    assert label == "country"


def test_execute_query(window, qtbot):
    window.query_combo.setCurrentIndex(0)
    country_input = window.params_form.itemAt(0, QFormLayout.ItemRole.FieldRole).widget()
    country_input.setText("Brasil")
    qtbot.mouseClick(window.run_btn, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(lambda: "Dados retornados" in window.statusBar().currentMessage(), timeout=3000)


def test_invalid_query(window, qtbot):
    window.query_combo.setCurrentIndex(1)
    start_date_input = window.params_form.itemAt(0, QFormLayout.ItemRole.FieldRole).widget()
    end_date_input = window.params_form.itemAt(1, QFormLayout.ItemRole.FieldRole).widget()
    start_date_input.setText("2023-01-01")
    end_date_input.setText("2023-12-31")

    def mock_execute_query(query_name, params):
        raise ValueError("Erro simulado")

    window.controller.execute_query = mock_execute_query
    qtbot.mouseClick(window.run_btn, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(lambda: "Erro simulado" in window.statusBar().currentMessage(), timeout=3000)