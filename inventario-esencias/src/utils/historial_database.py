"""
Base de datos separada para el historial de ventas
Esto permite eliminar productos sin restricciones de integridad referencial
"""
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class HistorialVenta(Base):
    __tablename__ = 'historial_ventas'

    id = Column(String, primary_key=True)
    id_producto = Column(String, nullable=False)  # Sin foreign key
    nombre_producto = Column(String, nullable=False)  # Guardamos el nombre
    genero_producto = Column(String, nullable=False, default='Unisex')  # Guardamos el género
    cantidad_vendida = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    fecha_venta = Column(DateTime, nullable=False, default=datetime.now)
    cliente = Column(String, nullable=True)
    ganancia = Column(Float, nullable=False, default=0.0)
    
    # Información del producto al momento de la venta (snapshot)
    costo_por_ml_momento = Column(Float, nullable=False)  # Costo por ml al momento de la venta
    proveedor_momento = Column(String, nullable=False)   # Proveedor al momento de la venta

DATABASE_URL_HISTORIAL = 'sqlite:///historial_ventas.db'

def get_historial_engine():
    return create_engine(DATABASE_URL_HISTORIAL)

def create_historial_tables():
    engine = get_historial_engine()
    Base.metadata.create_all(engine)

def get_historial_session():
    engine = get_historial_engine()
    Session = sessionmaker(bind=engine)
    return Session()
