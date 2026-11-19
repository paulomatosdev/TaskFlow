from flask_wtf import FlaskForm


def strip(valor):
    return valor.strip() if isinstance(valor, str) else valor


def strip_ou_none(valor):
    return strip(valor) or None


def normalizar_email(valor):
    return valor.strip().lower() if isinstance(valor, str) else valor


class ApiForm(FlaskForm):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        csrf = False
