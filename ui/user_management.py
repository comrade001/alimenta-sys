from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QListWidget
from database import session, User


class UserManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(100, 100, 500, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Buscador
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or employee ID")
        self.search_input.textChanged.connect(self.search_users)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Lista de usuarios
        self.user_list = QListWidget()
        self.load_users()
        layout.addWidget(self.user_list)

        # Formulario para detalles del usuario
        form_layout = QVBoxLayout()

        # Campos de nombre
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter first name")
        form_layout.addWidget(QLabel("First Name:"))
        form_layout.addWidget(self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter last name")
        form_layout.addWidget(QLabel("Last Name:"))
        form_layout.addWidget(self.last_name_input)

        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("Enter middle name")
        form_layout.addWidget(QLabel("Middle Name (optional):"))
        form_layout.addWidget(self.middle_name_input)

        # ID de empleado
        self.employee_id_input = QLineEdit()
        self.employee_id_input.setPlaceholderText("Enter employee ID")
        form_layout.addWidget(QLabel("Employee ID:"))
        form_layout.addWidget(self.employee_id_input)

        # Número de tarjeta
        self.card_number_input = QLineEdit()
        self.card_number_input.setPlaceholderText("Enter card number")
        form_layout.addWidget(QLabel("Card Number:"))
        form_layout.addWidget(self.card_number_input)

        layout.addLayout(form_layout)

        # Botones de acción
        button_layout = QHBoxLayout()

        add_button = QPushButton("Add User")
        add_button.clicked.connect(self.add_user)
        button_layout.addWidget(add_button)

        update_button = QPushButton("Update User")
        update_button.clicked.connect(self.update_user)
        button_layout.addWidget(update_button)

        delete_button = QPushButton("Delete User")
        delete_button.clicked.connect(self.delete_user)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_users(self):
        """Load users into the list widget."""
        self.user_list.clear()
        users = session.query(User).all()
        for user in users:
            self.user_list.addItem(f"{user.employee_id} - {user.first_name} {user.last_name}")

    def search_users(self):
        """Filter users based on search input."""
        search_term = self.search_input.text().lower()
        self.user_list.clear()
        users = session.query(User).filter(
            (User.first_name.ilike(f"%{search_term}%")) |
            (User.last_name.ilike(f"%{search_term}%")) |
            (User.employee_id.ilike(f"%{search_term}%"))
        ).all()
        for user in users:
            self.user_list.addItem(f"{user.employee_id} - {user.first_name} {user.last_name}")

    def add_user(self):
        """Add a new user to the database."""
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        middle_name = self.middle_name_input.text()
        employee_id = self.employee_id_input.text()
        card_number = self.card_number_input.text()

        if not first_name or not last_name or not employee_id or not card_number:
            QMessageBox.warning(self, "Input Error", "Please complete all mandatory fields.")
            return

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            employee_id=employee_id,
            card_number=card_number
        )
        session.add(new_user)
        session.commit()

        QMessageBox.information(self, "Success", "User added successfully.")
        self.load_users()
        self.clear_form()

    def update_user(self):
        """Update the selected user's information."""
        selected_item = self.user_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Please select a user to update.")
            return

        employee_id, _ = selected_item.text().split(" - ")
        user = session.query(User).filter_by(employee_id=employee_id).first()

        if user:
            user.first_name = self.first_name_input.text()
            user.last_name = self.last_name_input.text()
            user.middle_name = self.middle_name_input.text()
            user.employee_id = self.employee_id_input.text()
            user.card_number = self.card_number_input.text()
            session.commit()
            QMessageBox.information(self, "Success", "User updated successfully.")
            self.load_users()
            self.clear_form()

    def delete_user(self):
        """Delete the selected user from the database."""
        selected_item = self.user_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Please select a user to delete.")
            return

        employee_id, _ = selected_item.text().split(" - ")
        user = session.query(User).filter_by(employee_id=employee_id).first()

        if user:
            session.delete(user)
            session.commit()
            QMessageBox.information(self, "Success", "User deleted successfully.")
            self.load_users()
            self.clear_form()

    def clear_form(self):
        """Clear the input fields."""
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.middle_name_input.clear()
        self.employee_id_input.clear()
        self.card_number_input.clear()
