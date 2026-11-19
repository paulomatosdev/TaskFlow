from flask import Blueprint

tasks = Blueprint("tasks", __name__, url_prefix="/tasks")

from app.tasks import routes  # noqa: E402, F401  (no fim para evitar import circular)
