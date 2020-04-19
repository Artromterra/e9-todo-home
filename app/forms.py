from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
	username = StringField('Пользователь', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	remember_me = BooleanField('Запомнить меня')
	submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
	username = StringField('Пользователь', validators=[DataRequired()])
	email = StringField('Почта', validators=[DataRequired(), Email()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	password2 = PasswordField(
		'Повторить пароль', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Зарегистрироваться')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Пожалуйста введите другое имя.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Пожалуйста введите другой адрес почты.')

class TodoForm(FlaskForm):
	topic = StringField('Тема', validators=[
		DataRequired()])
	body = TextAreaField('Описание', validators=[
		DataRequired()])
	time_end = DateField(
		'Дата окончания', format='%Y-%m-%d')
	submit = SubmitField('Отправить')
