from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QComboBox, \
    QListWidget
from database import session, Menu, Shift
import datetime


class MenuManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Management")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # Lista de ítems de menú
        self.menu_list = QListWidget()
        self.load_menu_items()
        layout.addWidget(self.menu_list)

        # Formulario de detalles del menú
        form_layout = QVBoxLayout()

        # Campo de nombre del ítem de menú
        self.item_name_input = QLineEdit()
        self.item_name_input.setPlaceholderText("Enter menu item name")
        form_layout.addWidget(QLabel("Menu Item Name:"))
        form_layout.addWidget(self.item_name_input)

        # Selección de turno
        self.shift_combo = QComboBox()
        self.load_shifts()
        form_layout.addWidget(QLabel("Select Shift:"))
        form_layout.addWidget(self.shift_combo)

        # Disponibilidad
        self.availability_combo = QComboBox()
        self.availability_combo.addItems(["Available", "Out of Stock"])
        form_layout.addWidget(QLabel("Availability:"))
        form_layout.addWidget(self.availability_combo)

        layout.addLayout(form_layout)

        # Botones de acción
        button_layout = QHBoxLayout()

        add_button = QPushButton("Add Menu Item")
        add_button.clicked.connect(self.add_menu_item)
        button_layout.addWidget(add_button)

        update_button = QPushButton("Update Menu Item")
        update_button.clicked.connect(self.update_menu_item)
        button_layout.addWidget(update_button)

        delete_button = QPushButton("Delete Menu Item")
        delete_button.clicked.connect(self.delete_menu_item)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Conectar el evento de selección
        self.menu_list.itemSelectionChanged.connect(self.load_menu_item_to_form)

    def load_menu_item_to_form(self):
        """Load selected menu item's data into the form for editing."""
        selected_item = self.menu_list.currentItem()
        if not selected_item:
            return

        # Extraer el nombre del ítem de menú desde el texto del elemento seleccionado
        item_name = selected_item.text().split(" - ")[0]
        menu_item = session.query(Menu).filter_by(item_name=item_name).first()

        if menu_item:
            # Rellenar los campos del formulario con los datos del ítem de menú seleccionado
            self.item_name_input.setText(menu_item.item_name)
            shift_index = self.shift_combo.findData(menu_item.shift_id)
            self.shift_combo.setCurrentIndex(shift_index)
            availability_index = self.availability_combo.findText(menu_item.availability)
            self.availability_combo.setCurrentIndex(availability_index)

    def load_shifts(self):
        """Load shifts into the shift combo box."""
        shifts = session.query(Shift).all()
        self.shift_combo.clear()
        for shift in shifts:
            self.shift_combo.addItem(
                f"{shift.name} ({shift.start_time.strftime('%H:%M')} - {shift.end_time.strftime('%H:%M')})", shift.id)

    def load_menu_items(self):
        """Load menu items into the list widget."""
        self.menu_list.clear()
        menu_items = session.query(Menu).all()
        for item in menu_items:
            shift = session.query(Shift).filter_by(id=item.shift_id).first()
            shift_name = shift.name if shift else "No Shift"
            self.menu_list.addItem(f"{item.item_name} - {shift_name} - {item.availability}")

    def add_menu_item(self):
        """Add a new menu item to the database."""
        item_name = self.item_name_input.text()
        availability = self.availability_combo.currentText()
        shift_id = self.shift_combo.currentData()

        if not item_name:
            QMessageBox.warning(self, "Input Error", "Please enter a menu item name.")
            return

        # Verificar si un ítem de menú con el mismo nombre y turno ya existe
        existing_item = session.query(Menu).filter_by(item_name=item_name, shift_id=shift_id).first()
        if existing_item:
            QMessageBox.warning(self, "Duplicate Error",
                                "A menu item with this name already exists for the selected shift.")
            return

        new_item = Menu(
            item_name=item_name,
            availability=availability,
            shift_id=shift_id,
            created_at=datetime.datetime.utcnow()
        )
        session.add(new_item)
        session.commit()

        QMessageBox.information(self, "Success", "Menu item added successfully.")
        self.load_menu_items()
        self.clear_form()

    def update_menu_item(self):
        """Update the selected menu item's information."""
        selected_item = self.menu_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Please select a menu item to update.")
            return

        item_name = self.item_name_input.text()
        availability = self.availability_combo.currentText()
        shift_id = self.shift_combo.currentData()

        # Obtener el nombre original del ítem de menú seleccionado en la lista
        original_item_name = selected_item.text().split(" - ")[0]
        menu_item = session.query(Menu).filter_by(item_name=original_item_name).first()

        if menu_item:
            # Verificar si otro ítem de menú tiene el mismo nombre en el mismo turno
            duplicate_item = session.query(Menu).filter(
                (Menu.item_name == item_name),
                (Menu.shift_id == shift_id),
                Menu.id != menu_item.id  # Excluir el ítem de menú actual
            ).first()

            if duplicate_item:
                QMessageBox.warning(self, "Duplicate Error",
                                    "A menu item with this name already exists for the selected shift.")
                return

            # Actualizar el ítem de menú si no hay duplicados
            menu_item.item_name = item_name
            menu_item.availability = availability
            menu_item.shift_id = shift_id
            session.commit()

            QMessageBox.information(self, "Success", "Menu item updated successfully.")
            self.load_menu_items()
            self.clear_form()

    def delete_menu_item(self):
        """Delete the selected menu item from the database."""
        selected_item = self.menu_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Please select a menu item to delete.")
            return

        item_name_text = selected_item.text().split(" - ")[0]
        menu_item = session.query(Menu).filter_by(item_name=item_name_text).first()

        if menu_item:
            session.delete(menu_item)
            session.commit()
            QMessageBox.information(self, "Success", "Menu item deleted successfully.")
            self.load_menu_items()
            self.clear_form()

    def clear_form(self):
        """Clear the input fields."""
        self.item_name_input.clear()
        self.availability_combo.setCurrentIndex(0)
