import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError
from flask import Flask, jsonify, request

app = Flask(__name__)

BUCKET_NAME = os.getenv("BUCKET_NAME", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

s3_client = boto3.client("s3", region_name=AWS_REGION)


def _require_bucket_name():
    if not BUCKET_NAME:
        return (
            jsonify(
                {
                    "error": "BUCKET_NAME nao definido.",
                    "hint": "Defina a variavel de ambiente BUCKET_NAME antes de iniciar a API.",
                }
            ),
            500,
        )
    return None


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/files")
def list_files():
    missing_bucket_response = _require_bucket_name()
    if missing_bucket_response:
        return missing_bucket_response

    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    except ClientError as error:
        return (
            jsonify(
                {
                    "error": "Falha ao listar objetos no S3.",
                    "details": str(error),
                }
            ),
            500,
        )

    items = []
    for obj in response.get("Contents", []):
        items.append(
            {
                "key": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"].isoformat(),
            }
        )

    return jsonify({"bucket": BUCKET_NAME, "count": len(items), "files": items})


@app.post("/files")
def upload_file():
    missing_bucket_response = _require_bucket_name()
    if missing_bucket_response:
        return missing_bucket_response

    payload = request.get_json(silent=True) or {}

    content = payload.get("content")
    filename = payload.get("filename")

    if not content:
        return jsonify({"error": "Campo 'content' e obrigatorio."}), 400

    if not filename:
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        filename = f"note-{now}.txt"

    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=content.encode("utf-8"),
            ContentType="text/plain; charset=utf-8",
        )
    except ClientError as error:
        return (
            jsonify(
                {
                    "error": "Falha ao enviar arquivo para o S3.",
                    "details": str(error),
                }
            ),
            500,
        )

    return (
        jsonify(
            {
                "message": "Upload concluido.",
                "bucket": BUCKET_NAME,
                "key": filename,
            }
        ),
        201,
    )


if __name__ == "__main__":
    # host 0.0.0.0 permite acesso externo (ex.: do seu computador local)
    app.run(host="0.0.0.0", port=5000)
