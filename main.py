import sys
from PyQt6.QtWidgets import QApplication
from frontend.gui import QueryWindow
from controller.query_controller import QueryController
from utils.logging_config import setup_logging

def main():
    setup_logging()  # Configura o logging
    app = QApplication(sys.argv)
    controller = QueryController(disable_queries=True)
    window = QueryWindow(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()