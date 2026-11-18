from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


def _strip(valor):
    return valor.strip() if isinstance(valor, str) else valor


def _normalizar_email(valor):
    return valor.strip().lower() if isinstance(valor, str) else valor


class ApiForm(FlaskForm):
    class Meta:  
        csrf = False


class RegisterForm(ApiForm):
    name = StringField("Nome", filters=[_strip], validators=[DataRequired(), Length(max=100)])
    email = EmailField("E-mail", filters=[_normalizar_email], validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField("Confirmar senha", validators=[DataRequired(), EqualTo("password", message="As senhas não coincidem.")])
    


class LoginForm(ApiForm):
    email = EmailField("E-mail", filters=[_normalizar_email], validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Lembrar de mim")
