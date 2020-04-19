from app import db, login
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	todos = db.relationship('Todo', backref='author', lazy='dynamic')
	
	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	topic = db.Column(db.String(64))
	created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
	body = db.Column(db.String(256))
	time_end = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Todo {}>'.format(self.topic)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))