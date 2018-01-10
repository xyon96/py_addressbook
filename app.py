from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, pprint
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///py_addressbook.sqlite'
db = SQLAlchemy(app)

class Address(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.String(120))
  address = db.Column(db.String(512))

  def __init__(self, user, address):
    self.user = user
    self.address = address

class AddressSchema(Schema):
  class Meta:
    fields = ('id', 'user', 'address')

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)

@app.route("/users", methods=["GET"])
def get_users():
  all_users = Address.query.all()
  result = addresses_schema.dump(all_users)
  return jsonify(result.data)

@app.route("/users/<id>", methods=["POST"])
def add_user(id):
  new_user = Address(id, request.json['address'])
  db.session.add(new_user)
  db.session.commit()

# Hello World example
#@app.route("/")
#def hello():
#    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)

