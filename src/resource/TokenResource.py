import hashlib

from adapter.repository.TokenRepositoryPostgres import TokenRepositoryPostgres
from . import app
from flask.views import MethodView
from flask import jsonify, request, abort
from flask_jwt_extended import create_access_token


class TokenResource(MethodView):
    def __init__(self):
        self.repository = TokenRepositoryPostgres()

    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if username is None or password is None:
            abort(400)
        user = self.repository.find_one_by_username(username)
        if user is None or not self.check_password(password, bytes(user['password']), bytes(user['salt'])):
            abort(403)

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    @staticmethod
    def check_password(user_password, saved_password, salt):
        return saved_password == hashlib.pbkdf2_hmac('sha256', user_password.encode('utf-8'), salt, 100000, dklen=128)


toke_resource = TokenResource.as_view('toke_resource')
app.add_url_rule('/login', view_func=toke_resource, methods=['POST', ])
