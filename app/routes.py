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
def health():
    return jsonify({"status": "ok"})


@main.get("/about")
def about():
    return jsonify({"message": "Sobre o TaskFlow API", "status": "ok"})

@main.get("/contact")
def contacts():
    return jsonify({"message": "Contatos do TaskFlow API", "status": "ok"})

@main.get("/tasks/<int:task_id>")
def get_task(task_id):
    return jsonify({"message": f"Detalhes da tarefa {task_id}", "status": "ok"})
