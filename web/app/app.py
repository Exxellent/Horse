from flask import Flask, render_template, flash
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required



app = Flask(__name__)
application = app
client = app.test_client()
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

from models import Horse, Jockey, Stat_race
from auth import bp as auth_bp, init_login_manager, check_rights


init_login_manager(app)
app.register_blueprint(auth_bp)
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jockey_stat")
def jockey():
    jockeys = Jockey.query.order_by(Jockey.number_of_races.desc())
    return render_template("jockey_stat.html", jockeys=jockeys)

@app.route("/horse_stat")
def horse():
    horses = Horse.query.order_by(Horse.count_win.desc())
    return render_template("horse_stat.html", horses=horses)

@app.route("/stat_race")
def stat_race():
    stat_race = Stat_race.query.all()
    return render_template("stat_race.html", stat_race=stat_race)

@app.route("/add_race")
@login_required
@check_rights()
def add_race():
    return render_template("add_race.html")

   
