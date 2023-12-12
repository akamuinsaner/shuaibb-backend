from shuaibb.settings import ENV_CONFIG
from qcloud_cos import CosConfig
from dotenv import dotenv_values
from qcloud_cos import CosS3Client

def upload_to_cos(file, file_path):
    cos_config = CosConfig(
        Region=ENV_CONFIG["Region"],
        SecretId=ENV_CONFIG["SecretId"],
        SecretKey=ENV_CONFIG["SecretKey"],
        Token=ENV_CONFIG["Token"],
        Scheme=ENV_CONFIG["Scheme"]
    )
    client = CosS3Client(cos_config)
    response = client.put_object(
        Bucket = ENV_CONFIG["Bucket"],
        Body=file,
        Key=file_path,
    )
    return response if response is not None else None
