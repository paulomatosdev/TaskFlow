from flask_wtf.csrf import CSRFError

from app.responses import erro


def csrf_invalido(e):
    return erro("Token CSRF ausente ou inválido.", 400, {"csrf_token": [e.description]})


def erro_interno(e):
    # Nunca devolve a exceção original (SQL, nomes de tabelas, constraints...).
    return erro("Erro interno do servidor.", 500)

def erro_404(e):
    return erro("Recurso não encontrado.", 404)


def registrar_handlers(app):
    app.register_error_handler(CSRFError, csrf_invalido)
    app.register_error_handler(500, erro_interno)
    app.register_error_handler(404, erro_404)

