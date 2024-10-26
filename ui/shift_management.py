from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QTimeEdit, \
    QComboBox, QListWidget, QSpinBox, QListWidgetItem
from PyQt5.QtCore import QTime
from database import session, Shift
from datetime import time
from PyQt5.QtCore import Qt

class ShiftManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shift Management")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # Lista de turnos
        self.shift_list = QListWidget()
        layout.addWidget(self.shift_list)

        # Formulario de detalles del turno
        form_layout = QVBoxLayout()

        # Campo de nombre del turno
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter shift name")
        form_layout.addWidget(QLabel("Shift Name:"))
        form_layout.addWidget(self.name_input)

        # Día de la semana
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        form_layout.addWidget(QLabel("Day of the Week:"))
        form_layout.addWidget(self.day_combo)

        # Hora de inicio
        self.start_time_input = QTimeEdit()
        self.start_time_input.setDisplayFormat("HH:mm")
        form_layout.addWidget(QLabel("Start Time:"))
        form_layout.addWidget(self.start_time_input)

        # Hora de fin
        self.end_time_input = QTimeEdit()
        self.end_time_input.setDisplayFormat("HH:mm")
        form_layout.addWidget(QLabel("End Time:"))
        form_layout.addWidget(self.end_time_input)

        # Límite de comidas
        self.meal_limit_input = QSpinBox()
        self.meal_limit_input.setMinimum(1)
        self.meal_limit_input.setValue(1)
        form_layout.addWidget(QLabel("Meal Limit:"))
        form_layout.addWidget(self.meal_limit_input)

        layout.addLayout(form_layout)

        # Botones de acción
        button_layout = QHBoxLayout()

        add_button = QPushButton("Add Shift")
        add_button.clicked.connect(self.add_shift)
        button_layout.addWidget(add_button)

        update_button = QPushButton("Update Shift")
        update_button.clicked.connect(self.update_shift)
        button_layout.addWidget(update_button)

        delete_button = QPushButton("Delete Shift")
        delete_button.clicked.connect(self.delete_shift)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.load_shifts()

        # Conectar el evento de selección
        self.shift_list.currentRowChanged.connect(self.load_shift_to_form)

    def load_shift_to_form(self):
        """Load selected shift's data into the form for editing."""
        selected_row = self.shift_list.currentRow()
        if selected_row < 0:
            return

        selected_item = self.shift_list.item(selected_row)
        if not selected_item:
            return

        # Obtener el id del turno desde los datos de usuario almacenados
        shift_id = selected_item.data(Qt.UserRole)
        shift = session.query(Shift).filter_by(id=shift_id).first()

        if shift:
            # Rellenar los campos del formulario con los datos del turno seleccionado
            self.name_input.setText(shift.name)
            self.day_combo.setCurrentIndex(shift.day_of_week)
            self.start_time_input.setTime(QTime(shift.start_time.hour, shift.start_time.minute))
            self.end_time_input.setTime(QTime(shift.end_time.hour, shift.end_time.minute))
            self.meal_limit_input.setValue(shift.meal_limit)

    def load_shifts(self):
        """Load shifts into the list widget."""
        self.shift_list.clear()
        shifts = session.query(Shift).all()
        for shift in shifts:
            day_of_week = self.day_combo.itemText(shift.day_of_week)

            # Formatear start_time y end_time para mostrar solo horas y minutos
            start_time_str = shift.start_time.strftime("%H:%M")
            end_time_str = shift.end_time.strftime("%H:%M")

            item = QListWidgetItem(
                f"{shift.name} - {day_of_week} ({start_time_str} - {end_time_str}) - Limit: {shift.meal_limit}")
            item.setData(Qt.UserRole, shift.id)  # Guardar el id del turno en el rol de usuario
            self.shift_list.addItem(item)

    def check_overlap(self, day_of_week, start_time, end_time, exclude_shift_id=None):
        """
        Check for overlapping shifts on the same day.
        If exclude_shift_id is provided, ignore that shift during the check (useful for updates).
        """
        overlapping_shifts = session.query(Shift).filter(
            Shift.day_of_week == day_of_week,
            Shift.start_time < end_time,
            Shift.end_time > start_time
        )

        if exclude_shift_id:
            overlapping_shifts = overlapping_shifts.filter(Shift.id != exclude_shift_id)

        return overlapping_shifts.first() is not None

    def add_shift(self):
        """Add a new shift to the database."""
        name = self.name_input.text()
        day_of_week = self.day_combo.currentIndex()
        start_time = time(self.start_time_input.time().hour(), self.start_time_input.time().minute())
        end_time = time(self.end_time_input.time().hour(), self.end_time_input.time().minute())
        meal_limit = self.meal_limit_input.value()

        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a shift name.")
            return

        # Verificar que el horario de inicio no sea igual al de fin
        if start_time == end_time:
            QMessageBox.warning(self, "Invalid Time", "Start time and end time cannot be the same.")
            return

        # Verificar que los horarios no se traslapen
        if self.check_overlap(day_of_week, start_time, end_time):
            QMessageBox.warning(self, "Schedule Overlap", "This shift overlaps with an existing shift.")
            return

        new_shift = Shift(
            name=name,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            meal_limit=meal_limit
        )
        session.add(new_shift)
        session.commit()

        QMessageBox.information(self, "Success", "Shift added successfully.")
        self.load_shifts()
        self.clear_form()

    def update_shift(self):
        """Update the selected shift's information."""
        selected_item = self.shift_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Please select a shift to update.")
            return

        name = self.name_input.text()
        day_of_week = self.day_combo.currentIndex()
        start_time = time(self.start_time_input.time().hour(), self.start_time_input.time().minute())
        end_time = time(self.end_time_input.time().hour(), self.end_time_input.time().minute())
        meal_limit = self.meal_limit_input.value()

        # Verificar que el horario de inicio no sea igual al de fin
        if start_time == end_time:
            QMessageBox.warning(self, "Invalid Time", "Start time and end time cannot be the same.")
            return

        shift_name = selected_item.text().split(" - ")[0]
        shift = session.query(Shift).filter_by(name=shift_name).first()

        if shift:
            # Verificar que los horarios no se traslapen, excluyendo el turno actual
            if self.check_overlap(day_of_week, start_time, end_time, exclude_shift_id=shift.id):
                QMessageBox.warning(self, "Schedule Overlap", "This shift overlaps with an existing shift.")
                return

            shift.name = name
            shift.day_of_week = day_of_week
            shift.start_time = start_time
            shift.end_time = end_time
            shift.meal_limit = meal_limit
            session.commit()
            QMessageBox.information(self, "Success", "Shift updated successfully.")
            self.load_shifts()
            self.clear_form()

    def delete_shift(self):
        """Delete the selected shift from the database."""
        selected_item = self.shift_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Please select a shift to delete.")
            return

        shift_name = selected_item.text().split(" - ")[0]
        shift = session.query(Shift).filter_by(name=shift_name).first()

        if shift:
            session.delete(shift)
            session.commit()
            QMessageBox.information(self, "Success", "Shift deleted successfully.")
            self.load_shifts()
            self.clear_form()

    def clear_form(self):
        """Clear the input fields."""
        self.name_input.clear()
        self.start_time_input.setTime(QTime(0, 0))
        self.end_time_input.setTime(QTime(0, 0))
        self.meal_limit_input.setValue(1)
