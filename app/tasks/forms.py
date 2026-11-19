from wtforms import DateField, StringField, TextAreaField
from wtforms.validators import AnyOf, DataRequired, Length, Optional

from app.auth.forms import ApiForm, _strip

PRIORIDADES = ("baixa", "media", "alta")


def _strip_ou_none(valor):
    valor = _strip(valor)
    return valor or None


class TaskForm(ApiForm):
    title = StringField("Título", filters=[_strip],
                        validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Descrição", filters=[_strip_ou_none],
                                validators=[Optional()])
    priority = StringField("Prioridade", filters=[_strip_ou_none],
                           validators=[Optional(), AnyOf(PRIORIDADES)])
    due_date = DateField("Data de vencimento", format="%Y-%m-%d",
                         validators=[Optional()])
    category = StringField("Categoria", filters=[_strip_ou_none],
                           validators=[Optional(), Length(max=50)])
