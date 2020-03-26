from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init DB
db = SQLAlchemy(app)
#init MARSHMALLOW
ma = Marshmallow(app)

# Birthday Model
class BDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    fname = db.Column(db.String(100))
    date = db.Column(db.DateTime)

    def __init__(self, name, fname, date):
        self.name = name
        self.fname = fname
        self.date = date

# BDay Schema
class BDaySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'fname', 'date')

# Init Schema
bday_schema = BDaySchema()
bdays_schema = BDaySchema(many=True)

# Create a BDay
@app.route('/bday', methods=['POST'])
def addBDay():
    name = request.json['name']
    fname = request.json['fname']
    date = request.json['date']

    newBDay = BDay(name, fname, datetime(int(date[:4]), int(date[5:7]), int(date[8:10])))

    db.session.add(newBDay)
    db.session.commit()

    return bday_schema.jsonify(newBDay)

# Get All BDay
@app.route('/bday', methods=['GET'])
def get_bdays():
    all_bday = BDay.query.all()
    result = bdays_schema.dump(all_bday)
    return jsonify(result)

# Get One BDay
@app.route('/bday/<id>', methods=['GET'])
def get_bday(id):
    bday = BDay.query.get(id)
    return bday_schema.jsonify(bday)

# Delete Bday
@app.route('/bday/<id>', methods=['DELETE'])
def delete_bday(id):
    bday = BDay.query.get(id)

    db.session.delete(bday)
    db.session.commit()

    return bday_schema.jsonify(bday)

# Update a BDay
@app.route('/bday/<id>', methods=['PUT'])
def update_product(id):
  bday = BDay.query.get(id)

  name = request.json['name']
  fname = request.json['fname']
  date = request.json['date']

  bday.name = name
  bday.fname = fname
  bday.date = datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))

  db.session.commit()

  return bday_schema.jsonify(bday)

# Run server
if __name__ == '__main__':
    app.run(debug=True)