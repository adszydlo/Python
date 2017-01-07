from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.request import urlopen, urljoin

import geocoder
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Place(object):
    def meters_to_walking_time(self, meters):
        # powiedzmy ze predkosc chodu to 80m/min
        return int(meters / 80)

    def wiki_path(self, slug):
        return urljoin("http://pl.wikipedia.org/wiki/", slug.replace(' ', '_'))

    def address_to_latlng(self, address):
        g = geocoder.google(address)
        return (g.lat, g.lng)

    def queryAddress(self, address):
        lat, lng = self.address_to_latlng(address)

        query_url = 'https://pl.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(
            lat, lng)
        g = urlopen(query_url)
        results = g.read().decode('utf8')
        g.close()

        data = json.loads(results)

        places = []
        for place in data['query']['geosearch']:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lon']

            wiki_url = self.wiki_path(name)
            walking_time = self.meters_to_walking_time(meters)

            d = {
                'name': name,
                'url': wiki_url,
                'time': walking_time,
                'lat': lat,
                'lng': lng
            }

            places.append(d)

        return places

    def query(self, lat, lng):
        query_url = 'https://pl.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(
            lat, lng)
        g = urlopen(query_url)
        results = g.read().decode('utf8')
        g.close()

        data = json.loads(results)

        places = []
        for place in data['query']['geosearch']:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lon']

            wiki_url = self.wiki_path(name)
            walking_time = self.meters_to_walking_time(meters)

            d = {
                'name': name,
                'url': wiki_url,
                'time': walking_time,
                'lat': lat,
                'lng': lng
            }

            places.append(d)

        return places