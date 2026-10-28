from flask import Blueprint, jsonify


main = Blueprint("main", __name__)


@main.get("/")
def index():
    return jsonify(
        {
            "message": "TaskFlow API está funcionando.",
            "status": "ok",
        }
    )


@main.get("/health")
def health_check():
    return jsonify({"status": "healthy"})
