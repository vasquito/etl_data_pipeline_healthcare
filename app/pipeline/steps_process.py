from app.pipeline.steps import dataset_to_s3, download_from_dataset, s3_to_sqlite
from app.utils.s3_utils import BUCKET_MEDICAL_CENTRALS

def step_download_from_dataset() -> dict:
    url = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/ministerio-de-salud/centros-medicos-barriales/centros_medicos_barriales.geojson"
    base_name = "data"

    result = download_from_dataset.process(url, base_name)
    return result


def step_dataset_to_s3(data) -> dict:
    bucket = BUCKET_MEDICAL_CENTRALS
    prefix = "datasets"

    result = dataset_to_s3.process(data, bucket, prefix)
    return result


def step_s3_to_sqlite(filename: str) -> dict:
    bucket = BUCKET_MEDICAL_CENTRALS
    prefix = "datasets"

    result = s3_to_sqlite.process(filename, bucket, prefix)
    return result


