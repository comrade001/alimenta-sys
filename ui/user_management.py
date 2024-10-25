# ui/user_management.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from database import session, User

class UserManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Usuarios")

        layout = QVBoxLayout()

        # Ejemplo de campos para añadir usuario
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del Usuario")
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.name_input)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID de Empleado")
        layout.addWidget(QLabel("ID de Empleado:"))
        layout.addWidget(self.id_input)

        # Botón para guardar usuario
        self.save_button = QPushButton("Guardar Usuario")
        self.save_button.clicked.connect(self.save_user)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_user(self):
        # Crear nuevo usuario y guardar en la base de datos
        name = self.name_input.text()
        employee_id = self.id_input.text()
        new_user = User(name=name, employee_id=employee_id)
        session.add(new_user)
        session.commit()
