from wtforms import BooleanField, EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.forms import ApiForm, normalizar_email, strip


class RegisterForm(ApiForm):
    name = StringField("Nome", filters=[strip], validators=[DataRequired(), Length(max=100)])
    email = EmailField("E-mail", filters=[normalizar_email],
                       validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField("Confirmar senha", validators=[
        DataRequired(), EqualTo("password", message="As senhas não coincidem.")])


class LoginForm(ApiForm):
    email = EmailField("E-mail", filters=[normalizar_email], validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Lembrar de mim")
