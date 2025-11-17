import sys, os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if root not in sys.path:
    sys.path.append(root)

import boto3
import os
from app.utils.s3_utils import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, LOCALSTACK_ENDPOINT, exist_file

def process(filename, bucket, prefix="datasets") -> dict:
    try:
        s3_path = f"{prefix}/{filename}"
        if exist_file(bucket, s3_path):
            print("[S3] Ya fue descargado y subido al s3.", flush=True)
            result = {
                 "desc": "[S3] Ya fue descargado y subido al s3.",
                 "status": "warning",
                 "alert_type": "warning",
                 "continue": True
            }
            return result

        # Subir a S3
        s3 = boto3.client("s3",
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY,
                          region_name=AWS_REGION,
                          endpoint_url=LOCALSTACK_ENDPOINT)

        s3.upload_file(filename, bucket, s3_path)

        # Eliminar archivo local
        os.remove(filename)

        # Registrar historial en SQLite
        # descargas.registrar_descarga(url, fecha)

        print(f"[S3] JSON subido a S3 como s3://{bucket}/{s3_path}", flush=True)
        result = {
            "filename": filename,
            "desc": f"[S3] JSON subido a S3 como s3://{bucket}/{s3_path}",
            "status": "ok",
            "alert_type": "info",
            "continue": True
        }
        return result

    except Exception as e:
        # Registrar historial en SQLite
        # descargas.registrar_descarga(url, fecha)

        print("Error process:", e, flush=True)
        result = {
            "desc": f"[S3] Se ha producido un error en el proceso: {e}",
            "status": "error",
            "alert_type": "danger",
            "continue": False
        }
        return result
