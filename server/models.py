from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    serialize_rules = ('-signups.camper',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer)

    signups = db.relationship('Signup',backref = 'camper')

    @validates('name')
    def validate_age(self,key,name):
        names = Camper.query.filter_by(name = name).first()
        if not name:
            raise ValueError('Name does not exist.')
        elif name in names:
            raise ValueError('Name already exists.')
        return name
    
    @validates('age')
    def validate_age(self,key,age):
        if type(age) != int or age <8 or age > 18:
            raise ValueError('Invalid age input.')
        return age

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-signups.activity',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    signups = db.relationship('Signup',backref = 'activity')

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    serialize_rules = ('-camper.signups','-activity.signups')

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    campers_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    @validates('time')
    def verify_time(self,key,time):
        if type(time) != int or time <0 or time > 23:
            raise ValueError('Invalid time input.')
        return time
