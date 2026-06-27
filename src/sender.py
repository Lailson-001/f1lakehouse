import os
import argparse
from pathlib import Path

import boto3
import dotenv
from tqdm import tqdm

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

if not AWS_KEY or not AWS_SECRET_KEY:
    raise ValueError("Credenciais AWS não encontradas no arquivo .env")


class Sender:
    def __init__(self, bucket_name, bucket_folder="results"):
        self.bucket_name = bucket_name
        self.bucket_folder = bucket_folder.rstrip("/")

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name="us-east-2",
        )

    def process_file(self, filename):
        file_name = Path(filename).name
        bucket_path = f"{self.bucket_folder}/{file_name}"

        try:
            self.s3.upload_file(
                Filename=filename,
                Bucket=self.bucket_name,
                Key=bucket_path,
            )

            print(f"Upload realizado: {bucket_path}")

        except Exception as err:
            print(f"Erro ao enviar {file_name}: {err}")
            return False

        os.remove(filename)
        return True

    def process_folder(self, folder):
        if not os.path.isdir(folder):
            print(f"Pasta '{folder}' não existe.")
            return

        files = os.listdir(folder)

        for file in tqdm(files):
            filepath = os.path.join(folder, file)

            if os.path.isfile(filepath):
                self.process_file(filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--bucket",
        required=True,
        help="Nome do bucket S3",
    )

    parser.add_argument(
        "--bucket_path",
        default="results",
        help="Pasta dentro do bucket",
    )

    parser.add_argument(
        "--folder",
        default=str(DATA_DIR),
        help="Pasta local com os arquivos",
    )

    args = parser.parse_args()

    sender = Sender(
        bucket_name=args.bucket,
        bucket_folder=args.bucket_path,)

    sender.process_folder(args.folder)

parser.add_argument(
    "--bucket_path",
    default="f1-results-raw/results",
    type=str,
)
        











   


