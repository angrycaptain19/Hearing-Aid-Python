from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin

# Init server

app = Flask(__name__)

cors = CORS(app)

# MySQL confiurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:avk@localhost:3306/hearingAid'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

ma = Marshmallow(app)

# Users class ------------------------------------------------------------

class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	firstName = db.Column(db.String(50))
	lastName = db.Column(db.String(50))
	email = db.Column(db.String(50), unique = True)
	password = db.Column(db.String(50))
	age = db.Column(db.Integer)
	address = db.Column(db.String(50))
	isActive = db.Column(db.Boolean)    

	def __init__(self, firstName, lastName, email, password, age, address):
		self.firstName  = firstName 
		self.lastName = lastName
		self.email = email
		self.password = password
		self.age = age
		self.address = address
		self.isActive = True

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'paswword', 'age', 'address', 'isActive')

users_schema = UsersSchema()
many_users = UsersSchema(many=True)
# End Users class --------------------------------------------------------
    

# Routes -----------------------------------------------------------------    
@app.route('/user', methods = ['POST', 'GET'])
@cross_origin()
def userAddAndView():
	if request.method == 'POST':
		firstName = request.json['firstName']
		lastName = request.json['lastName']
		email = request.json['email']
		password =request.json['password']
		age = request.json['age']
		address = request.json['address']

		all_users = Users.query.all()
		for user in all_users:
			if user.email == email:
				return '[!] User already exists'
	
	
		user = Users(firstName, lastName, email, password, age, address)
		db.session.add(user)
		db.session.commit()

		return 'Added successfully'
	

	elif request.method == 'GET':
		users = Users.query.all()

		return many_users.jsonify(users)	

@app.route('/user/<id>', methods = ['DELETE', 'PUT', 'GET'])
def userUpdateAndDelete(id):
	if request.method == 'DELETE':
		user = Users.query.get(id)
		db.session.delete(user)
		db.session.commit()
		return f'User with {id} deleted successfully'
	elif request.method == 'PUT':
		return 'Working on it'
	elif request.method == 'GET':
		user = Users.query.get(id)
		return users_schema.jsonify(user)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
