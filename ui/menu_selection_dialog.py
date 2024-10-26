from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt

class MenuSelectionDialog(QDialog):
    def __init__(self, menu_items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Menu Item")
        self.selected_item = None
        self.setStyleSheet("QPushButton { font-size: 18px; padding: 15px; }")  # Botones grandes

        layout = QVBoxLayout()

        # Mensaje de instrucciones
        instruction_label = QLabel("Please select a menu item for this shift:")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("font-size: 20px;")  # Texto grande
        layout.addWidget(instruction_label)

        # GridLayout para los botones de ítems de menú
        button_layout = QGridLayout()
        button_layout.setSpacing(10)

        # Crear un botón para cada ítem de menú
        for row, item in enumerate(menu_items):
            button = QPushButton(item.item_name)
            button.clicked.connect(lambda _, item_id=item.id: self.select_item(item_id))
            button_layout.addWidget(button, row // 3, row % 3)  # 3 columnas

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def select_item(self, item_id):
        """Set selected menu item and close the dialog."""
        self.selected_item = item_id
        self.accept()  # Cierra el diálogo y confirma la selección
