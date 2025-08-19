from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(String, primary_key=True)  # Cambiado a String para IDs personalizados
    nombre = Column(String, nullable=False)
    stock_actual = Column(Float, nullable=False)  # Cambiado a Float para decimales
    costo_entrada = Column(Float, nullable=False)   # Cambiado de stock_minimo a costo_entrada
    proveedor = Column(String, nullable=False)
    fecha_caducidad = Column(Date, nullable=False)
    costo_por_ml = Column(Float, nullable=False)
    
    # Relación con Salidas
    salidas = relationship("Salida", back_populates="producto")

    def valor_total_stock(self):
        return self.stock_actual * self.costo_por_ml

    def stock_bajo(self):
        return self.stock_actual < 50  # Umbral fijo de 50ml

class Salida(Base):
    __tablename__ = 'salidas'

    id = Column(String, primary_key=True)
    id_producto = Column(String, ForeignKey('productos.id'), nullable=False)
    cantidad_vendida = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    fecha_venta = Column(DateTime, nullable=False, default=datetime.now)
    cliente = Column(String, nullable=True)
    ganancia = Column(Float, nullable=False, default=0.0)
    
    # Relación con Producto
    producto = relationship("Producto", back_populates="salidas")

DATABASE_URL = 'sqlite:///inventario.db'

def get_engine():
    return create_engine(DATABASE_URL)

def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()