import requests
import json
from datetime import datetime

def process(url, base_name) -> dict:
    try:
        fecha = datetime.now().strftime("%Y-%m-%d")
        filename = f"{base_name}_{fecha}.json"

        # Descargar JSON
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Guardar localmente
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Registrar historial en SQLite
        # workflow.registrar_descarga(filename, fecha, ok)

        print(f"Descargado como filename {filename}", flush=True)
        result = {
            "filename": filename,
            "desc": f"Descargado como filename {filename}",
            "status": "ok",
            "alert_type": "info",
            "continue": True
        }
        return result
    except Exception as e:
        # Registrar historial en SQLite
        # workflow.registrar_descarga(filename, fecha, error)
        print("Error process:", e, flush=True)
        result = {
            "desc": f"Se ha producido un error en el proceso: {e}",
            "status": "error",
            "alert_type": "danger",
            "continue": False
        }
        return result
