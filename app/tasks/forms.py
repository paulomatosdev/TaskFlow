from wtforms import DateField, StringField, TextAreaField
from wtforms.validators import AnyOf, DataRequired, Length, Optional

from app.forms import ApiForm, strip, strip_ou_none

PRIORIDADES = ("baixa", "media", "alta")
STATUS = ("pendente", "em_andamento", "concluida")


class TaskForm(ApiForm):
    title = StringField("Título", filters=[strip],
                        validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Descrição", filters=[strip_ou_none],
                                validators=[Optional()])
    priority = StringField("Prioridade", filters=[strip_ou_none],
                           validators=[Optional(), AnyOf(PRIORIDADES)])
    due_date = DateField("Data de vencimento", format="%Y-%m-%d",
                         validators=[Optional()])
    category = StringField("Categoria", filters=[strip_ou_none],
                           validators=[Optional(), Length(max=50)])
    
    
