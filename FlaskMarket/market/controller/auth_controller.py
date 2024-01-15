from flask import jsonify
from flask_login import login_user, logout_user, current_user

from market.models import User


class AuthController:

    @staticmethod
    def login(form_data):
        username = json_form_data['username']
        password = json_form_data['password']

        attempted_user = User.query.filter_by(username=username).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = password):
            login_user(attempted_user)
            return jsonify({
                    'message' : f'Sucess! You are logged in as: {attempted_user.username}'
            }), 200
        else:
            return jsonify({
                'message' : 'Login fail, please check your username and password'
            }), 401