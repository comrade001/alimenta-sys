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
    name = Column(String, nullable=False)
    employee_id = Column(String, unique=True, nullable=False)
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
    availability = Column(String, nullable=False)  # Ej. "Disponible" o "Agotado"
    shift_id = Column(Integer, ForeignKey('shifts.id'))  # Relación con turno
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    shift = relationship("Shift", back_populates="menu_items")


# Modelo de Consumo
class Consumption(Base):
    __tablename__ = 'consumptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    menu_id = Column(Integer, ForeignKey('menu.id'))
    shift_id = Column(Integer, ForeignKey('shifts.id'))
    consumed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")
    menu_item = relationship("Menu")
    shift = relationship("Shift")


# Crear tablas
Base.metadata.create_all(engine)
