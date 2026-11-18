from flask import jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm
from app.extensions import db, login_manager
from app.models import User


def _user_json(user):
    return {"id": user.id, "name": user.name, "email": user.email}


def _ok(status=200, **dados):
    return jsonify({"status": "ok", **dados}), status


def _erro(mensagem, status, errors=None):
    corpo = {"status": "error", "message": mensagem}
    return jsonify(corpo | {"errors": errors} if errors else corpo), status


@auth.before_request
def exigir_json():  # substitui o token CSRF: outro site não envia JSON para cá sem CORS
    if request.method == "POST" and not request.is_json:
        return _erro("Envie os dados como JSON.", 415)


@login_manager.unauthorized_handler
def nao_autenticado():
    return _erro("Autenticação necessária.", 401)


@auth.post("/register")
def register():
    form = RegisterForm()
    if not form.validate_on_submit():
        return _erro("Dados inválidos.", 400, form.errors)
    user = User(name=form.name.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    return _ok(201, user=_user_json(user))


@auth.post("/login")
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return _erro("Dados inválidos.", 400, form.errors)
    user = db.session.scalar(db.select(User).filter_by(email=form.email.data))
    if user is None or not user.check_password(form.password.data):
        return _erro("E-mail ou senha inválidos.", 401)  
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
