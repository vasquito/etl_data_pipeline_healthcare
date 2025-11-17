import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if root not in sys.path:
    sys.path.append(root)

import graphviz
import panel as pn
from pandas import DataFrame
from app.db.sqlite.audit_etl import get_all_audit_etl

pn.extension()

def render_etl_diagram(status: dict):
    dot = graphviz.Digraph(graph_attr={'rankdir': 'LR'})
    dot.attr('node', shape='rectangle')
    dot.attr(colorscheme='greens9')

    node_etl(dot, "A", "Download \n from Dataset BA", status["descarga"], "Descarga los datos desde dataset BA")
    node_etl(dot, "B", "Upload \n to AWS S3", status["s3"], "Guarda archivo descargado en bucket S3")
    node_etl(dot, "C", "Load \n into SQLite", status["sqlite"], "Ingesta de datos en SQLite")
    node_etl(dot, "D", "Completed", status["completado"], "Guarda archivo en bucket S3")

    dot.edge("A", "B", style='dashed', tooltip="Paso 1: Descarga → S3")
    dot.edge("B", "C", style='dashed', tooltip="Paso 2: S2 → SQLite")
    dot.edge("C", "D", style='dashed', tooltip="Paso 3: SQLite → Completado")

    # Renderiza a archivo SVG y lo carga como ruta
    #path = dot.render(filename='grafo_test', format='svg', cleanup=True)
    #return pn.pane.SVG(path, sizing_mode="stretch_width")

    # Renderiza en la memoria
    svg_code = dot.pipe(format='svg').decode('utf-8')
    return pn.pane.HTML(svg_code, sizing_mode="stretch_width")


def node_etl(dot, id, label, status_desc, toolpit=None):
    colors = {
        "ok": ("#388e3c", "white", " ✅"),             # verde éxito
        "error": ("#f44336", "white", " 🟥️"),          # rojo error
        "warning": ("#ff7043", "black", "⚠️"),
        "processing": ("darkblue", "white", " ⏳"),     # azul técnico
        "completed": ("#388e3c", "white", " 🎉")
    }
    fill, font, image = colors.get(status_desc, ("lightgray", "black", " ⏳"))
    dot.node(id, label + "\n" + image, style="filled", fillcolor=fill, fontcolor=font, toolpit=toolpit)


def render_etl_table() -> DataFrame:
    df = get_all_audit_etl()
    df_renamed = df.rename(columns={
        "date": "Fecha",
        "node1": "Download",
        "node2": "S3",
        "node3": "Sqlite",
        "node4": "Completado",
        "result": "Resultado"
    })
    df_filtered = df_renamed.drop(columns=["id"])

    return df_filtered