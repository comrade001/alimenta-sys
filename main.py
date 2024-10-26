# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, QMdiSubWindow
from database import session, User, Menu, Consumption
from ui.user_management import UserManagement

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AlimentaSys - Gestión de Comedor")
        self.resize(800, 600)

        # Configurar área MDI
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        # Crear menú
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Archivo")

        # Acción para registrar usuarios
        user_action = QAction("Usuarios", self)
        user_action.triggered.connect(self.manage_users)
        file_menu.addAction(user_action)

        # Acción para gestionar el menú diario
        menu_action = QAction("Menú Diario", self)
        menu_action.triggered.connect(self.manage_menu)
        file_menu.addAction(menu_action)

        # Acción para registrar consumos
        consumption_action = QAction("Consumos", self)
        consumption_action.triggered.connect(self.record_consumption)
        file_menu.addAction(consumption_action)

    def manage_users(self):
        sub = QMdiSubWindow()
        sub.setWidget(UserManagement())
        sub.setWindowTitle("User Management")
        self.mdi.addSubWindow(sub)
        sub.show()

    def manage_menu(self):
        sub = QMdiSubWindow()
        sub.setWindowTitle("Gestión del Menú Diario")
        # Aquí puedes importar y conectar tu módulo de gestión del menú
        self.mdi.addSubWindow(sub)
        sub.show()

    def record_consumption(self):
        sub = QMdiSubWindow()
        sub.setWindowTitle("Registrar Consumo")
        # Aquí puedes importar y conectar tu módulo de consumo
        self.mdi.addSubWindow(sub)
        sub.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
