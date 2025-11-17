import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if root not in sys.path:
    sys.path.append(root)

import json
import boto3
import pandas as pd
from app.db.sqlite.medical_centers import delete_medical_centers, insert_dataframe
from app.utils.s3_utils import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, LOCALSTACK_ENDPOINT, exist_file


def process(filename, bucket, prefix="datasets") -> dict:
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY,
                          region_name=AWS_REGION,
                          endpoint_url=LOCALSTACK_ENDPOINT)
        s3_path = f"{prefix}/{filename}"
        if exist_file(bucket, s3_path):
            obj = s3.get_object(Bucket=bucket, Key=s3_path)
            geojson_data = json.loads(obj["Body"].read().decode("utf-8"))

            registros = []
            for f in geojson_data["features"]:
                props = f["properties"]
                lon, lat = f["geometry"]["coordinates"]
                props["lat"] = lat
                props["lon"] = lon
                registros.append(props)

            df = pd.DataFrame(registros)
            # Me aseguro de que las columnas estén completas y limpias
            df_centers = df.fillna("").drop_duplicates().reset_index(drop=True)

            if not df_centers.empty:
                delete_medical_centers()
                insert_dataframe(df_centers)

            result = {
                "desc": f"[Sqlite] Datos almacenados en Datalake",
                "status": "ok",
                "alert_type": "info",
                "continue": True
            }
            return result
        else:
            result = {
                "desc": f"[Sqlite] No existe el archivo {filename} en S3",
                "status": "error",
                "alert_type": "danger",
                "continue": False
            }
            return result

    except Exception as e:
        print("Error process:", e, flush=True)
        result = {
            "desc": f"[Sqlite] Se ha producido un error en el proceso: {e}",
            "status": "error",
            "alert_type": "danger",
            "continue": False
        }
        return result



