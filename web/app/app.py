from flask import Flask, render_template, flash, request, redirect, url_for
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate


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
migrate = Migrate(app, db)
from models import Horse, Jockey, Stat_race, Upcoming_races, Race_horse, Race_jockey
from auth import bp as auth_bp, init_login_manager, check_rights


init_login_manager(app)
app.register_blueprint(auth_bp)
    
@app.route("/")
def index():
    jockeys = Race_jockey.query.all()
    horses = Race_horse.query.all()
    races = Upcoming_races.query.all()

    return render_template("index.html", jockeys=jockeys, horses=horses, races=races)

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

@app.route("/add_race", methods=['GET', 'POST'])
@login_required
@check_rights()
def add_race():
    horses = Horse.query.all()
    jockeys = Jockey.query.all()
    
    if request.method == 'POST':
        try:
            horses = request.form.getlist('horses')
            jockeys = request.form.getlist('jockeys')
            date = request.form.get('date')
            race = Upcoming_races()
            race.date=date
            db.session.add(race)
            db.session.commit()
            race = Upcoming_races.query.order_by(Upcoming_races.id.desc()).first()
            for horse in horses:
                i = Race_horse()
                i.id_race=race.id
                i.name_horse=Horse.query.filter(Horse.id == int(horse)).first().name
                db.session.add(i)
            for jockey in jockeys:
                i = Race_jockey()
                i.id_race=race.id
                i.name_jockey=Jockey.query.filter(Jockey.id == int(jockey)).first().full_name
                db.session.add(i)
            db.session.commit()
        except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'При добавлении данных произошла ошибка. \n{e}', category='danger')
        return redirect(url_for('index'))
        
        
    return render_template("add_race.html", horses=horses, jockeys=jockeys)

   
