from shuaibb.settings import ENV_BASE_DIR
from qcloud_cos import CosConfig
from dotenv import dotenv_values
from qcloud_cos import CosS3Client

def upload_to_cos(file, file_path):
    config = {**dotenv_values(ENV_BASE_DIR / ".env.txcloud")}
    cos_config = CosConfig(
        Region=config["Region"],
        SecretId=config["SecretId"],
        SecretKey=config["SecretKey"],
        Token=config["Token"],
        Scheme=config["Scheme"]
    )
    client = CosS3Client(cos_config)
    response = client.put_object(
        Bucket = config["Bucket"],
        Body=file,
        Key=file_path,
    )
    return response if response is not None else None
