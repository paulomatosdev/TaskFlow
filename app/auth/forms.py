from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.extensions import db
from app.models import User


def _strip(valor):
    return valor.strip() if isinstance(valor, str) else valor


def _normalizar_email(valor):
    return valor.strip().lower() if isinstance(valor, str) else valor


class ApiForm(FlaskForm):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        csrf = False  # API JSON: a proteção é exigir JSON (ver routes.py)


class RegisterForm(ApiForm):
    name = StringField("Nome", filters=[_strip], validators=[DataRequired(), Length(max=100)])
    email = EmailField("E-mail", filters=[_normalizar_email],
                       validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField("Confirmar senha", validators=[
        DataRequired(), EqualTo("password", message="As senhas não coincidem.")])

    def validate_email(self, field):
        if db.session.scalar(db.select(User).filter_by(email=field.data)):
            raise ValidationError("Este e-mail já está cadastrado.")


class LoginForm(ApiForm):
    email = EmailField("E-mail", filters=[_normalizar_email], validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Lembrar de mim")
