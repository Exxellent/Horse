import functools
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


from models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')




def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

def load_user(user_id):
    user = User.query.get(user_id)
    return user

def check_rights():
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            if not current_user.is_admin:
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))
            return function(*args, **kwargs)
        return wrapper
    return decorator

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно аутентифицированы.', 'success')
                next = request.args.get('next')
                return render_template('auth/login.html')
        flash('Неправильный логин или пароль','danger')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
