from flask import Flask, render_template, request, session, redirect, url_for
from Models import db, User, Place
from Forms import SignupForm, LoginForm, AddressForm

import requests
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flaskapp'
db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
  if 'email' in session:
    return redirect(url_for('home'))
  else:
    return render_template("index.html", session=session)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form, session=session)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('home'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if 'email' in session:
    return redirect(url_for('home'))

  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("login.html", form=form)
    else:
      email = form.email.data
      password = form.password.data

      user = User.query.filter_by(email=email).first()
      if user is not None and user.check_password(password):
        session['email'] = form.email.data
        return redirect(url_for('home'))
      else:
        return redirect(url_for('login'))

  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
  if 'email' not in session:
    return redirect(url_for('login'))

  form = AddressForm()

  places = []

  #pobranie aktualnej lokalizacji urzadzenia na podstawie IP
  send_url = 'http://freegeoip.net/json'
  r = requests.get(send_url)
  j = json.loads(r.text)
  lat = j['latitude']
  lng = j['longitude']
  #my_coordinates = (50.288706,18.6750773)
  my_coordinates = (lat, lng)

  if request.method == "POST":
      if form.validate() == False:
          return render_template("home.html", form=form)
      else:
          # pobranie adresu
          address = form.address.data

          # miejsca w okolicy adresu (z GeoDataAPI)
          p = Place()
          my_coordinates = p.address_to_latlng(address)
          places = p.queryAddress(address)

          # przesłanie wyników
          return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)


  elif request.method == 'GET':
      p = Place()
      places = p.query(lat, lng)
      return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)


if __name__ == "__main__":
  app.run(debug=True)