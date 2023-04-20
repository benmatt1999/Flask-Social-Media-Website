import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from forms import AddPup, DelPup, AddOwner

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

###########################
###### MODELS #############
###########################

class Puppy(db.Model):
    __tablename__ = 'puppies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    owner = db.relationship('Owner', backref='puppy', uselist=False)

    def __init__(self, name):
        self.name=name

    def __repr__(self):
        if self.owner:
            return f"Puppy is named {self.name} and their owner is {self.owner.name}!"
        else:
            return f"Puppy is named {self.name} and has no owner yet!"

class Owner(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name, pup_id):
        self.name=name
        self.puppy_id=pup_id

    def __repr__(self):
        return f"Owner name is {self.name}"

############################
###### View Functions ######
############################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_pup',methods=['GET', 'POST'])
def add_pup():
    form = AddPup()

    if form.validate_on_submit():
        name = form.name.data
        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('list_pups'))
    return render_template('add_pup.html', form=form)

@app.route('/delete_pup', methods=['GET', 'POST'])
def delete_pup():
    form = DelPup()

    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pups'))
    return render_template('delete_pup.html', form=form)

@app.route('/list_pups')
def list_pups():
    puppies = Puppy.query.all()
    return render_template('list_pups.html', puppies=puppies)

@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    form = AddOwner()

    if form.validate_on_submit():
        name = form.name.data
        pup_id = form.id.data
        new_owner = Owner(name, pup_id)
        db.session.add(new_owner)
        db.session.commit()

        return redirect(url_for('list_pups'))
    return render_template('add_owner.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
