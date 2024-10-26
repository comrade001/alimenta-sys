from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///alimentasys.db')
Session = sessionmaker(bind=engine)
session = Session()


# Modelo de Usuario
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)  # Nombre
    last_name = Column(String, nullable=False)  # Apellido Paterno
    middle_name = Column(String)  # Apellido Materno (puede ser opcional)
    employee_id = Column(String, unique=True, nullable=False)
    card_number = Column(String, unique=True, nullable=False)  # Número de tarjeta (único)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Modelo de Turno
class Shift(Base):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Ej. "Mañana", "Tarde"
    day_of_week = Column(Integer, nullable=False)  # 0=Domingo, 1=Lunes, ..., 6=Sábado
    start_time = Column(Time, nullable=False)  # Hora de inicio del turno
    end_time = Column(Time, nullable=False)  # Hora de fin del turno
    meal_limit = Column(Integer, default=1)  # Límite de comidas por turno

    # Relación con el menú
    menu_items = relationship("Menu", back_populates="shift")


# Modelo de Menú actualizado
class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    availability = Column(String, nullable=False)  # Ejemplo: "Disponible" o "Agotado"
    shift_id = Column(Integer, ForeignKey('shifts.id'))  # Relación con turno
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    shift = relationship("Shift", back_populates="menu_items")


class Consumption(Base):
    __tablename__ = 'consumptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_name = Column(String)  # Almacenar el nombre completo del usuario en el momento del consumo
    menu_id = Column(Integer, ForeignKey('menu.id'))
    menu_item_name = Column(String)  # Almacenar el nombre del ítem del menú en el momento del consumo
    shift_id = Column(Integer, ForeignKey('shifts.id'))
    shift_name = Column(String)  # Almacenar el nombre del turno en el momento del consumo
    consumed_at = Column(DateTime, default=datetime.datetime.utcnow)



# Crear tablas
Base.metadata.create_all(engine)
