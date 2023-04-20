from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class AddPup(FlaskForm):
    name = StringField("What is the puppy's name?")
    submit = SubmitField('Add Pup')

class DelPup(FlaskForm):
    id = IntegerField("What is the id of the pup?")
    submit = SubmitField('Remove Pup')

class AddOwner(FlaskForm):
    name = StringField("What is the owner's name")
    id = IntegerField("What is the Id of this owner's pup?")
    submit = SubmitField('Add Owner')
