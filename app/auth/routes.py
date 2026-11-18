from flask import request
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf.csrf import generate_csrf
from sqlalchemy.exc import IntegrityError

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm
from app.extensions import db, login_manager
from app.models import User
from app.responses import erro as _erro, ok as _ok


EMAIL_DUPLICADO = "Este e-mail já está cadastrado."


def _email_cadastrado(email):
    return db.session.scalar(db.select(User.id).filter_by(email=email)) is not None


def _user_json(user):
    return {"id": user.id, "name": user.name, "email": user.email}


@auth.before_request
def exigir_json():  # roda depois da checagem CSRF global
    if request.method == "POST" and not request.is_json:
        return _erro("Envie os dados como JSON.", 415)


@login_manager.unauthorized_handler
def nao_autenticado():
    return _erro("Autenticação necessária.", 401)


@auth.get("/csrf-token")
def csrf_token():
    
    return _ok(csrf_token=generate_csrf())


@auth.post("/register")
def register():
    form = RegisterForm()
    if not form.validate_on_submit():
        return _erro("Dados inválidos.", 400, form.errors)
    email = form.email.data
    if _email_cadastrado(email):  # caminho comum: evita um INSERT que vai falhar
        return _erro(EMAIL_DUPLICADO, 409, {"email": [EMAIL_DUPLICADO]})

    user = User(name=form.name.data, email=email)
    user.set_password(form.password.data)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:

        db.session.rollback()

        if _email_cadastrado(email):
            return _erro(EMAIL_DUPLICADO, 409, {"email": [EMAIL_DUPLICADO]})
        raise
    return _ok(201, user=_user_json(user))


@auth.post("/login")
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return _erro("Dados inválidos.", 400, form.errors)
    user = db.session.scalar(db.select(User).filter_by(email=form.email.data))
    if user is None or not user.check_password(form.password.data):
        return _erro("E-mail ou senha inválidos.", 401)  # mesma msg: não revela e-mails
    login_user(user, remember=form.remember.data)
    return _ok(user=_user_json(user))


@auth.post("/logout")
@login_required
def logout():
    logout_user()
    return _ok(message="Sessão encerrada.")


@auth.get("/me")
@login_required
def me():
    return _ok(user=_user_json(current_user))
