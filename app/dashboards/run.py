import sys, os
print("Iniciando app....", file=sys.stdout, flush=True)

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root not in sys.path:
    sys.path.append(root)
import config
import app.utils.sqlite_init  # Esto ejecuta init_once automáticamente
from app.utils.s3_utils import create_localstack_s3_bucket, BUCKET_MEDICAL_CENTRALS
create_localstack_s3_bucket(BUCKET_MEDICAL_CENTRALS)

import panel as pn
from pages import main, medical_centers_etl
from pages.medical_centers_etl import MedicalCentersEtl
from pages.medical_centers_graph import MedicalCentersGraph
from pages.medical_centers_map import MedicalCentersMap
from pages.medical_centers_table import MedicalCentersTable
from app.db.sqlite.medical_centers import find_all

pn.extension()

# Cargar dataframe y crear las vistas
df = find_all()
etl_page = MedicalCentersEtl()

tabs = pn.Tabs(
    ("🏠 Inicio", main.view()),
    ("⚙️ ETL", etl_page.view()),
    ("📋 Tabla", MedicalCentersTable(df).view()),
    ("📊 Graficos", MedicalCentersGraph(df).view()),
    ("🌍 Mapa", MedicalCentersMap(df).view()),
    dynamic=True  # permite que se actualicen si son funciones
)

# Ahora inyecto la referencia en la instancia
etl_page.tabs = tabs

# Mostrar la primera pestaña por defecto
tabs.active = 0

# Template con título y toggle
template = pn.template.FastListTemplate(
    title="",
    header=[pn.Row(pn.pane.Markdown("## 🩺 ETL-Dashboard: CABA - Centros Medicos Barriales"))],
    main=[tabs]
)

template.servable()
