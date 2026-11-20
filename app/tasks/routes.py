from flask import request
from flask_login import current_user, login_required

from app.extensions import db
from app.models.task import Task
from app.responses import erro as _erro, ok as _ok
from app.tasks import tasks
from app.tasks.forms import TaskForm


@tasks.before_request
def exigir_json():
    if request.method == "POST" and not request.is_json:
        return _erro("Envie os dados como JSON.", 415)


def _task_json(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "status": task.status,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "category": task.category,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }


def _buscar_task_por_id(task_id):
    # Tarefa inexistente ou de outro usuário -> 404 (não revela que o id existe).
    return db.first_or_404(db.select(Task).filter_by(id=task_id, user_id=current_user.id))


@tasks.get("/<int:task_id>")
@login_required
def detalhar_task(task_id):
    return _ok(task=_task_json(_buscar_task_por_id(task_id)))


@tasks.post("")  # com o url_prefix, vira POST /tasks
@login_required
def create_task():
    form = TaskForm()
    if not form.validate_on_submit():
        return _erro("Dados inválidos.", 400, form.errors)

    task = Task(
        title=form.title.data,
        description=form.description.data,
        priority=form.priority.data or "media",
        due_date=form.due_date.data,
        category=form.category.data,
        user_id=current_user.id,
    )
    db.session.add(task)
    db.session.commit()

    return _ok(201, task=_task_json(task))
