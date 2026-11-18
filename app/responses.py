from flask import jsonify


def ok(status=200, **dados):
    return jsonify({"status": "ok", **dados}), status


def erro(mensagem, status, errors=None):
    corpo = {"status": "error", "message": mensagem}
    return jsonify(corpo | {"errors": errors} if errors else corpo), status
