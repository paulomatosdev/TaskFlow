from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.get("/")
def index():
    return jsonify({"message": "TaskFlow API está funcionando.", "status": "ok"})


@main.get("/about")
def about():
    return jsonify({"message": "Sobre o TaskFlow API", "status": "ok"})


@main.get("/contact")
def contacts():
    return jsonify({"message": "Contatos do TaskFlow API", "status": "ok"})


