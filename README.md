
# AlimentaSys

**AlimentaSys** is a desktop application designed to manage industrial cafeteria services, specifically for companies providing food services within plant facilities. **AlimentaSys** allows users to identify employees, manage daily menus by shift, register meal consumption, and generate general consumption reports.

## Features

- **User Management**: Register, edit, and delete employees who use the cafeteria service.
- **Shift-Based Menu Management**: Configure and control the menu available for each defined shift, set by specific hours and days.
- **Consumption Tracking with Shift Limits**: Register meals consumed by users with a configurable limit per shift.
- **Shift Management**: Manage cafeteria shifts with customizable meal limits and defined days and hours.
- **General Reporting**: Provides general reports based on the transactional data in the consumption table.

## Technology Stack

- **Python 3**: Main programming language for the project.
- **SQLite**: Local database for data persistence.
- **SQLAlchemy**: ORM used to manage database operations.
- **PyQt5**: Framework used for building the graphical user interface (GUI).

## Screenshots

![Main Window](path/to/screenshot.png)  
*Description of the main window with MDI area.*

## Installation

To install and run **AlimentaSys**, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AlimentaSys.git
cd AlimentaSys
```

### 2. Set up a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note**: Ensure PyQt5 and SQLAlchemy are installed. If you encounter compatibility issues, you can install them manually:
> ```bash
> pip install PyQt5 SQLAlchemy
> ```

## Running the Application

To start the application, run the following command from the project’s root directory:

```bash
python main.py
```

## Project Structure

```plaintext
AlimentaSys/
├── main.py                # Entry point for the application
├── database.py            # Database configuration and SQLAlchemy models
├── ui/                    # Graphical user interfaces
│   ├── main_window.py     # Main window with MDI area
│   ├── user_management.py # User management module
│   ├── menu_management.py # Shift-based menu management module
│   ├── shift_management.py # Shift management module
│   └── consumption.py     # Consumption registration module
├── reports/               # Report generation logic
└── resources/             # Configuration files, icons, and other assets
```

### Key Files

- **`main.py`**: Application entry point, configuring the main window and MDI area.
- **`database.py`**: Database configuration and SQLAlchemy model definitions (`User`, `Menu`, `Consumption`, and `Shift`).
- **`ui/`**: Contains modules for each functionality (users, daily menu per shift, consumption, and shift management).

## Usage

1. **User Management**:
   - Add, edit, and delete employees.
   - Each employee has a unique ID and name.

2. **Shift Management**:
   - Define shifts with specific hours and days of the week.
   - Set a meal consumption limit per shift.

3. **Shift-Based Menu Management**:
   - Configure the available menu items for each shift.
   - Items can be marked as “Available” or “Out of Stock.”

4. **Consumption Tracking**:
   - Register each user's daily meal consumption by shift.
   - Enforce meal limits per shift, as configured.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Developed by Abraham Solis Alvarez. For questions or comments, reach out at [solisalvarezabraham@gmail.com](solisalvarezabraham@gmail.com).

