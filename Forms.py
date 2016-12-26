from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
  first_name = StringField('Imię', validators=[DataRequired("Wpisz swoje imię.")])
  last_name = StringField('Nazwisko', validators=[DataRequired("Wpisz swoje nazwisko.")])
  email = StringField('Email', validators=[DataRequired("Wpisz swój adres email."), Email("Wpisz poprawny adres email.")])
  password = PasswordField('Hasło', validators=[DataRequired("Wpisz swoje hasło."), Length(min=6, message="Hasło musi mieć conajmniej 6 znaków.")])
  submit = SubmitField('Zarejestruj się')


class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired("Wpisz swój adres email."), Email("Wpisz proszę poprawny adres email.")])
  password = PasswordField('Hasło', validators=[DataRequired("Wpisz swoje hasło.")])
  submit = SubmitField("Zaloguj się")

class AddressForm(FlaskForm):
  address = StringField('Adres', validators=[DataRequired("Podaj adres.")])
  submit = SubmitField("Szukaj")