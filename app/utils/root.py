import sys, os

# --- CÓDIGO DE CORRECCIÓN: Agregar la raíz del proyecto al sys.path ---
# Ejemplo __file__ está en .../app/dashboards/pages/1_ETL.py
# '..', '..', '..' sube 3 niveles hasta la carpeta *que contiene* 'app'.

def add_project_root():
    root = os.path.abspath(os.path.dirname(__file__))
    # Solo lo añade si no está ya para evitar duplicados.
    if root not in sys.path:
        sys.path.append(root)

def add_project_root_nevel_1():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if root not in sys.path:
        sys.path.append(root)

def add_project_root_nevel_2():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if root not in sys.path:
        sys.path.append(root)

def add_project_root_nevel_3():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    if root not in sys.path:
        sys.path.append(root)