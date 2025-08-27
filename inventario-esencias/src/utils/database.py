import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(String, primary_key=True)  # Cambiado a String para IDs personalizados
    nombre = Column(String, nullable=False)
    genero = Column(String, nullable=False, default='Unisex')  # Nuevo campo género
    stock_actual = Column(Float, nullable=False)  # Cambiado a Float para decimales
    costo_entrada = Column(Float, nullable=False)   # Cambiado de stock_minimo a costo_entrada
    proveedor = Column(String, nullable=False)
    fecha_caducidad = Column(Date, nullable=False)
    costo_por_ml = Column(Float, nullable=False)
    tipo_producto = Column(String, nullable=False, default='esencia')  # 'esencia' o 'frasco'
    
    # Relación con Salidas (sin foreign key constraint para independencia)
    # salidas = relationship("Salida", back_populates="producto")

    def valor_total_stock(self):
        return self.stock_actual * self.costo_por_ml

    def stock_bajo(self):
        return self.stock_actual < 50  # Umbral fijo de 50ml

class Frasco(Base):
    __tablename__ = 'frascos'

    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    costo = Column(Float, nullable=False)
    capacidad_ml = Column(Float, nullable=False)  # Capacidad en ml
    stock_actual = Column(Integer, nullable=False, default=0)  # Cantidad de frascos
    
    def valor_total_stock(self):
        return self.stock_actual * self.costo

    def stock_bajo(self):
        return self.stock_actual < 10  # Umbral de 10 frascos

class Salida(Base):
    __tablename__ = 'salidas'

    id = Column(String, primary_key=True)
    id_producto = Column(String, nullable=False)  # Sin Foreign Key para independencia
    cantidad_vendida = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    fecha_venta = Column(DateTime, nullable=False, default=datetime.now)
    cliente = Column(String, nullable=True)
    ganancia = Column(Float, nullable=False, default=0.0)
    
    # Sin relación con Producto para mantener historial independiente
    # producto = relationship("Producto", back_populates="salidas")

import os
import sys

def get_database_path():
    """Obtiene la ruta de la base de datos considerando si es .exe o desarrollo"""
    if getattr(sys, 'frozen', False):
        # Si está ejecutándose como .exe
        try:
            # Intentar usar el directorio donde está el .exe
            exe_dir = os.path.dirname(sys.executable)
            db_path = os.path.join(exe_dir, 'inventario.db')
            
            # Verificar si tenemos permisos de escritura
            test_file = os.path.join(exe_dir, 'test_write.tmp')
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                return db_path
            except (PermissionError, OSError):
                # Si no tenemos permisos, usar Documents del usuario
                documents_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'InventarioEsencias')
                if not os.path.exists(documents_dir):
                    os.makedirs(documents_dir, exist_ok=True)
                return os.path.join(documents_dir, 'inventario.db')
        except Exception:
            # Como último recurso, usar Documents del usuario
            documents_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'InventarioEsencias')
            if not os.path.exists(documents_dir):
                os.makedirs(documents_dir, exist_ok=True)
            return os.path.join(documents_dir, 'inventario.db')
    else:
        # Si está ejecutándose en desarrollo
        # Obtener la ruta absoluta del directorio src
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)  # Subir un nivel desde utils/ a src/
        return os.path.join(src_dir, 'inventario.db')

DATABASE_PATH = get_database_path()
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

# Debug: Mostrar la ruta de la base de datos
print(f"DEBUG: Ruta de la base de datos: {DATABASE_PATH}")
print(f"DEBUG: ¿Es .exe? {getattr(sys, 'frozen', False)}")
print(f"DEBUG: URL de la base de datos: {DATABASE_URL}")

def get_engine():
    return create_engine(DATABASE_URL)

def create_tables():
    try:
        # Asegurar que el directorio existe
        db_dir = os.path.dirname(DATABASE_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"DEBUG: Directorio creado: {db_dir}")
        
        engine = get_engine()
        Base.metadata.create_all(engine)
        print(f"DEBUG: Tablas creadas exitosamente en: {DATABASE_PATH}")
        
        # Verificar si el archivo se creó
        if os.path.exists(DATABASE_PATH):
            print(f"DEBUG: Base de datos confirmada en: {DATABASE_PATH}")
        else:
            print(f"ERROR: No se pudo crear la base de datos en: {DATABASE_PATH}")
            
    except Exception as e:
        print(f"ERROR al crear tablas: {e}")
        print(f"ERROR: Ruta de base de datos: {DATABASE_PATH}")
        raise

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()