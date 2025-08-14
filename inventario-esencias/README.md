# Inventario de Esencias

Este proyecto es una aplicación de inventario para gestionar productos de esencias. La aplicación cuenta con una interfaz gráfica de usuario (GUI) que permite a los usuarios agregar, eliminar y actualizar productos en el inventario.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
inventario-esencias
├── src
│   ├── main.py                # Punto de entrada de la aplicación.
│   ├── models
│   │   ├── __init__.py        # Inicializa el paquete de modelos.
│   │   └── producto.py        # Define la clase Producto.
│   ├── views
│   │   ├── __init__.py        # Inicializa el paquete de vistas.
│   │   └── main_window.py     # Define la clase MainWindow.
│   ├── controllers
│   │   ├── __init__.py        # Inicializa el paquete de controladores.
│   │   └── inventario_controller.py # Define la clase InventarioController.
│   └── utils
│       ├── __init__.py        # Inicializa el paquete de utilidades.
│       └── database.py        # Funciones para manejar la base de datos.
├── requirements.txt           # Dependencias necesarias para el proyecto.
└── README.md                  # Documentación del proyecto.
```

## Instalación

Para instalar las dependencias necesarias, ejecute el siguiente comando:

```
pip install -r requirements.txt
```

## Ejecución

Para ejecutar la aplicación, utilice el siguiente comando:

```
python src/main.py
```

## Contribuciones

Las contribuciones son bienvenidas. Si desea contribuir, por favor abra un issue o un pull request en el repositorio.