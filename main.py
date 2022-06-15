from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DecimalField
from wtforms.validators import DataRequired, URL
import requests

app = Flask(__name__)
Bootstrap(app)

# DB connection information
# Todo - Hide secret key
app.config['SECRET_KEY'] = '8BYkEfBA6O6mth3sLXWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Database columns
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# Add new cafe form
class CafeForm(FlaskForm):
    cafe_name = StringField(label='Cafe Name', validators=[DataRequired()])
    map_url = StringField(label='Cafe Location on Google Maps (URL)',
                          validators=[DataRequired(),
                                      URL()])
    img_url = StringField(label='Cafe Image',
                          validators=[DataRequired(),
                                      URL()])
    location = StringField(label='Cafe Location')
    seats = StringField(label='Number of Seats')
    has_toilet = BooleanField(label='Has Toilets?')
    has_wifi = BooleanField(label='Wi-Fi Strength Rating')
    has_sockets = BooleanField(label='Has Sockets?')
    can_take_calls = BooleanField(label='Take Calls?')
    coffee_price = DecimalField(label='Coffee Price', places=2, rounding=None)
    submit = SubmitField(label='Submit')
    csrf_token = app.secret_key


# home page
@app.route("/")
def home():
    return render_template('index.html')


# all cafes
@app.route('/cafes')
def cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template('cafes.html', cafe_data=all_cafes)


# add cafe
@app.route("/add", methods=["GET", "POST"])
def add():
    form = CafeForm()
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form.get("cafe_name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("has_sockets")),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


# delete cafe
@app.route('/delete', methods=['GET', 'POST'])
def delete_cafe():
    cafe_id = request.args.get('id')
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# edit cafe
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    cafe_id = request.args.get('id')
    cafe_selected = Cafe.query.get(cafe_id)
    if request.method == 'POST':
        cafe_id = request.form['id']
        new_location = request.form.get('cafe_location')
        cafe_to_update = Cafe.query.get(cafe_id)
        cafe_to_update.rating = new_location
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', cafe=cafe_selected)


if __name__ == '__main__':
    app.run(debug=True)
