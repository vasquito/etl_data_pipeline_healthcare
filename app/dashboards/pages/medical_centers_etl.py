import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if root not in sys.path:
    sys.path.append(root)

import panel as pn
import time
from app.dashboards.utils.etl_renders import render_etl_diagram, render_etl_table
from app.pipeline.steps_process import step_download_from_dataset, step_dataset_to_s3, step_s3_to_sqlite
from app.db.sqlite.audit_etl import insert_audit_etl, delete_audit_etl
from app.db.sqlite.medical_centers import delete_medical_centers
from app.utils.s3_utils import limpiar_bucket, BUCKET_MEDICAL_CENTRALS
from app.dashboards.pages.medical_centers_graph import MedicalCentersGraph
from app.dashboards.pages.medical_centers_map import MedicalCentersMap
from app.dashboards.pages.medical_centers_table import MedicalCentersTable
from app.db.sqlite.medical_centers import find_all


class MedicalCentersEtl:
    def __init__(self, tabs=None):
        self.tabs = tabs
        self.grafo = None
        self.alert = None
        self.tabla = None
        self.result= None
        # "pending","ok","error","warning","completed"
        self.status = {
            "descarga": "pending",
            "s3": "pending",
            "sqlite": "pending",
            "completado": "pending",
        }

    def ejecutar_etl(self, event=None):
        global result
        # init
        self.grafo.object = render_etl_diagram(self.status).object

        # Run
        step = "descarga"
        filename = ""
        result_desc = ""
        try:
            self.alert.visible = True
            for paso in self.status:
                step = paso
                self.alert.object = f"Ejecutando: {step}"
                self.alert.alert_type = "info"
                match step:
                    case "descarga":
                        result = step_download_from_dataset()
                        time.sleep(1.5)  # Opcional
                        self.alert.alert_type = result["alert_type"]
                        self.alert.object = result["desc"]
                        self.status[step] = result["status"]
                        self.grafo.object = render_etl_diagram(self.status).object
                        filename = result["filename"]
                        if not result["continue"]:
                            break
                        if self.status[step] == "warning":
                            result_desc += self.alert.object + " | "

                    case "s3":
                        result = step_dataset_to_s3(filename)
                        time.sleep(1.5)  # Opcional
                        self.alert.alert_type = result["alert_type"]
                        self.alert.object = result["desc"]
                        self.status[step] = result["status"]
                        self.grafo.object = render_etl_diagram(self.status).object
                        if not result["continue"]:
                            break
                        if self.status[step] == "warning":
                            result_desc += self.alert.object + " | "

                    case "sqlite":
                        result = step_s3_to_sqlite(filename)
                        time.sleep(1.5)  # Opcional
                        self.alert.alert_type = result["alert_type"]
                        self.alert.object = "[Sqlite] Datos Cargados"  # result["desc"]
                        self.status[step] = result["status"]
                        self.grafo.object = render_etl_diagram(self.status).object
                        if not result["continue"]:
                            break
                        if self.status[step] == "warning":
                            result_desc += self.alert.object + " | "

                    case "completado":
                        time.sleep(1.5)  # Opcional
                        self.alert.alert_type = "success"
                        self.alert.object = "Proceso completado"
                        self.status[step] = "ok"
                        self.grafo.object = render_etl_diagram(self.status).object
                        result_desc += self.alert.object

                        df = find_all()
                        self.tabs[2] = ("📋 Tabla", MedicalCentersTable(df).view())
                        self.tabs[3] = ("📊 Gráficos", MedicalCentersGraph(df).view())
                        self.tabs[4] = ("🌍 Mapa", MedicalCentersMap(df).view())
                        break

                    case _:
                        self.alert.alert_type = "danger"
                        self.alert.object = "Error Critico: Job desconocido"
                        status = {
                            "descarga": "error",
                            "s3": "error",
                            "sqlite": "error",
                            "completado": "error",
                        }
                        self.grafo.object = render_etl_diagram(status).object
                        break

        except Exception as e:
            print(e, flush=True)
            status[step] = "error"
            self.alert.alert_type = "danger"
            self.alert.object = f"Error in the step[{step}] : {e}"
            self.grafo.object = render_etl_diagram(status).object
        finally:
            # alert.visible = False
            insert_audit_etl(
                self.status["descarga"].capitalize(),
                self.status["s3"].capitalize(),
                self.status["sqlite"].capitalize(),
                self.status["completado"].capitalize(),
                result_desc
            )
            self.tabla.value = render_etl_table()


    def ejecutar_clean(self, event=None):
        try:
            self.alert.visible = True
            self.alert.object = f"Ejecutando la limpieza de la BD y S3"
            self.alert.alert_type = "info"
            delete_medical_centers()
            delete_audit_etl()
            limpiar_bucket(BUCKET_MEDICAL_CENTRALS)
            df = find_all()
            self.tabs[2] = ("📋 Tabla", MedicalCentersTable(df).view())
            self.tabs[3] = ("📊 Gráficos", MedicalCentersGraph(df).view())
            self.tabs[4] = ("🌍 Mapa", MedicalCentersMap(df).view())

            self.alert.object = f"Limpieza completada"
        except Exception as e:
            print(e, flush=True)
            self.alert.alert_type = "warning"
            self.alert.object = f"Error en la limpieza : {e}"
        finally:
            self.status = {
                "descarga": "pending",
                "s3": "pending",
                "sqlite": "pending",
                "completado": "pending",
            }
            self.grafo.object = render_etl_diagram(self.status).object
            self.tabla.value = render_etl_table()

    def view(self):
        pn.extension('tabulator')

        #"pending","ok","error","warning","completed"
        self.status = {
            "descarga": "pending",
            "s3": "pending",
            "sqlite": "pending",
            "completado": "pending",
        }
        self.grafo = render_etl_diagram(self.status)
        self.alert = pn.pane.Alert("", alert_type="info", visible=False)

        # Tabla
        self.tabla = pn.widgets.Tabulator(
            render_etl_table(),
            configuration={
                "columns": [
                    {"title": "Fecha", "field": "Fecha", "editable": False},
                    {"title": "Download", "field": "Download", "editable": False},
                    {"title": "S3", "field": "S3", "editable": False},
                    {"title": "Sqlite", "field": "Sqlite", "editable": False},
                    {"title": "Resultado", "field": "Resultado", "editable": False}
                ]
            },
            pagination='remote',
            page_size=10,
            sizing_mode="stretch_width")
        self.tabla.show_index = False

        # Button Etl
        button_etl = pn.widgets.Button(name="Ejecutar ETL", button_type="primary")
        button_etl.on_click(self.ejecutar_etl)
        button_etl.width = 150

        # Limpieza a 0
        button_clean = pn.widgets.Button(name="Limpiar BD & S3", button_type="warning")
        button_clean.on_click(self.ejecutar_clean)
        button_clean.width = 150

        return pn.Column(
            pn.Row(
                pn.Column(pn.pane.Markdown("## ⚙️ Ingesta de Datos - Centros Médicos"),
                          self.grafo,
                          pn.Row(button_etl, pn.Spacer(width=10), button_clean),
                          self.alert,
                          sizing_mode="stretch_width"),
                pn.Column(pn.pane.Markdown("## 🧾 Auditoría"),
                          self.tabla,
                          sizing_mode="stretch_width"), # width=550
                    sizing_mode="stretch_width", align="start"),
            sizing_mode="stretch_width"
        )
