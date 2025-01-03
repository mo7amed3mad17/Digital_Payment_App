from flask import Blueprint, render_template, redirect, url_for, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.account import Account

ui_routes = Blueprint('ui', __name__)

@ui_routes.route('/')
@ui_routes.route('/home')
@ui_routes.route('/about')
def about():
    return render_template('about.html')


def login():
    return redirect(url_for('ui.login'))

@ui_routes.route('/login')
def login():
    return render_template('index.html')

@ui_routes.route('/register')
def register():
    return render_template('register.html')

@ui_routes.route('/account')
def account():
    return render_template('account.html')

@ui_routes.route('/profile')
def profile():
    return render_template('profile.html')

@ui_routes.route('/history')
def transaction_history():
    return render_template('history.html')

@ui_routes.route('/transfer')
def transfer():
    return render_template('transfer.html')

@ui_routes.route('/transfer-confirm')
def transfer_confirm():
    return render_template('/transfer-confirm.html')
