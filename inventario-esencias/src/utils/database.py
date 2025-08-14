from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(String, primary_key=True)  # Cambiado a String para IDs personalizados
    nombre = Column(String, nullable=False)
    stock_actual = Column(Float, nullable=False)  # Cambiado a Float para decimales
    stock_minimo = Column(Float, nullable=False)   # Cambiado a Float para decimales
    proveedor = Column(String, nullable=False)
    fecha_caducidad = Column(Date, nullable=False)
    costo_por_ml = Column(Float, nullable=False)

    def valor_total_stock(self):
        return self.stock_actual * self.costo_por_ml

    def stock_bajo(self):
        return self.stock_actual < self.stock_minimo

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