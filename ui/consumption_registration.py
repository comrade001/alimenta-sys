from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, \
    QDialog
from database import session, User, Shift, Consumption, Menu
from datetime import datetime, time, timedelta, date
from ui.menu_selection_dialog import MenuSelectionDialog

class ConsumptionRegistration(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consumption Registration")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Input para el número de tarjeta
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("Enter card number")
        self.card_input.returnPressed.connect(self.process_consumption)
        layout.addWidget(QLabel("Card Number:"))
        layout.addWidget(self.card_input)

        # Tabla para mostrar los consumos del último día
        self.consumption_table = QTableWidget()
        self.consumption_table.setColumnCount(4)
        self.consumption_table.setHorizontalHeaderLabels(["User", "Menu Item", "Shift", "Time"])
        layout.addWidget(self.consumption_table)

        self.setLayout(layout)
        self.load_today_consumptions()

    def detect_current_shift(self):
        """Detect the current shift based on the current time and day of the week."""
        current_time = datetime.now().time()
        current_day = datetime.now().weekday()  # Monday = 0, Sunday = 6

        # Buscar el turno activo para el día actual
        current_shift = session.query(Shift).filter(
            Shift.day_of_week == current_day,
            Shift.start_time <= current_time,
            Shift.end_time > current_time
        ).first()

        return current_shift

    def process_consumption(self):
        """Process consumption based on card number and current shift."""
        card_number = self.card_input.text()
        if not card_number:
            QMessageBox.warning(self, "Input Error", "Please enter a card number.")
            return

        # Buscar usuario por card_number
        user = session.query(User).filter_by(card_number=card_number).first()
        if not user:
            QMessageBox.warning(self, "User Not Found", "No user found with this card number.")
            return

        # Detectar el turno actual
        current_shift = self.detect_current_shift()
        if not current_shift:
            QMessageBox.warning(self, "No Active Shift", "There is no active shift at this time.")
            return

        # Verificar si el usuario ya ha consumido en el turno actual en el día de hoy
        today = date.today()
        existing_consumption = session.query(Consumption).filter(
            Consumption.user_id == user.id,
            Consumption.shift_id == current_shift.id,
            Consumption.consumed_at >= datetime.combine(today, time(0, 0)),
            Consumption.consumed_at < datetime.combine(today + timedelta(days=1), time(0, 0))
        ).first()

        if existing_consumption:
            QMessageBox.warning(self, "Already Consumed", "User has already consumed in this shift today.")
            return

        # Seleccionar ítems de menú disponibles para el turno
        available_menu_items = session.query(Menu).filter_by(shift_id=current_shift.id, availability="Available").all()
        if not available_menu_items:
            QMessageBox.warning(self, "No Menu Item Available", "There are no available menu items for this shift.")
            return

        # Si hay más de un ítem, permitir que el usuario elija
        if len(available_menu_items) > 1:
            dialog = MenuSelectionDialog(available_menu_items, self)
            if dialog.exec_() == QDialog.Accepted:
                selected_menu_id = dialog.selected_item
            else:
                QMessageBox.information(self, "Selection Canceled", "Menu selection was canceled.")
                return
        else:
            # Si solo hay un ítem, seleccionarlo automáticamente
            selected_menu_id = available_menu_items[0].id

        # Crear el registro de consumo con el ítem seleccionado
        new_consumption = Consumption(
            user_id=user.id,
            shift_id=current_shift.id,
            menu_id=selected_menu_id,
            consumed_at=datetime.now()
        )
        session.add(new_consumption)
        session.commit()

        QMessageBox.information(self, "Success", "Consumption registered successfully.")
        self.card_input.clear()
        self.load_today_consumptions()

    def load_today_consumptions(self):
        """Load today's consumptions into the table, displaying the latest entries at the top."""
        self.consumption_table.setRowCount(0)
        today = datetime.now().date()

        # Obtener los consumos del día de hoy, ordenados por hora en orden descendente
        consumptions = session.query(Consumption).filter(
            Consumption.consumed_at >= today
        ).order_by(Consumption.consumed_at.desc()).all()

        for row, consumption in enumerate(consumptions):
            user = session.query(User).filter_by(id=consumption.user_id).first()
            menu_item = session.query(Menu).filter_by(id=consumption.menu_id).first()
            shift = session.query(Shift).filter_by(id=consumption.shift_id).first()  # Obtener el turno asociado

            self.consumption_table.insertRow(row)
            self.consumption_table.setItem(row, 0, QTableWidgetItem(f"{user.first_name} {user.last_name}"))
            self.consumption_table.setItem(row, 1, QTableWidgetItem(menu_item.item_name))

            # Mostrar el nombre del turno
            shift_name = f"{shift.name} ({shift.start_time.strftime('%H:%M')} - {shift.end_time.strftime('%H:%M')})"
            self.consumption_table.setItem(row, 2, QTableWidgetItem(shift_name))

            # Hora del consumo
            self.consumption_table.setItem(row, 3, QTableWidgetItem(consumption.consumed_at.strftime("%H:%M")))

        # Ajustar solo la columna de turno
        self.consumption_table.resizeColumnToContents(2)  # La columna de turno es la columna 2