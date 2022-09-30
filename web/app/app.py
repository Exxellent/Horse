from flask import Flask, render_template, flash
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)


from auth import bp as auth_bp, init_login_manager


init_login_manager(app)
app.register_blueprint(auth_bp)
    
@app.route("/")
def index():
    return render_template("index.html")