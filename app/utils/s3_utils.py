import os
from app.utils.root import add_project_root
add_project_root()

import boto3
from botocore.exceptions import ClientError

LOCALSTACK_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:4566")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BUCKET_MEDICAL_CENTRALS = os.getenv("BUCKET_MEDICAL_CENTRALS", "centros-medicos-barriales")

def create_localstack_s3_bucket(bucket_name):
    """
    Creates an S3 bucket in LocalStack.
    """
    try:
        # Cliente S3
        s3_client = boto3.client(
            's3',
            region_name=AWS_REGION,
            endpoint_url=LOCALSTACK_ENDPOINT,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        s3_client.create_bucket(Bucket=bucket_name)
        print(f"S3 bucket '{bucket_name}' created successfully in LocalStack.", flush=True)
    except Exception as e:
        print(f"Error creating bucket: {e}", flush=True)


def limpiar_bucket(bucket_name):
    # Cliente S3
    s3_client = boto3.client(
        's3',
        region_name=AWS_REGION,
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    print(f"Limpiando bucket: {bucket_name}", flush=True)

    # Listar objetos
    objetos = s3_client.list_objects_v2(Bucket=bucket_name)
    if "Contents" in objetos:
        for obj in objetos["Contents"]:
            print(f"  - Eliminando: {obj['Key']}", flush=True)
            s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])
        print("Bucket limpiado correctamente", flush=True)
    else:
        print(" El bucket ya está vacío", flush=True)


def exist_file(bucket_name, key):
    s3_client = boto3.client('s3',
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY,
                    region_name=AWS_REGION,
                    endpoint_url=LOCALSTACK_ENDPOINT)

    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise e