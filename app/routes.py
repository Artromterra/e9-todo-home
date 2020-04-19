from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, TodoForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Todo
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
	todos = Todo.query.all()
	return render_template('index.html', title='Home Page', todos=todos)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = 'user/{}'.format(user.username)
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	todos = user.todos.all()
	form = TodoForm()
	if form.validate_on_submit():
		todo = Todo(
			topic=form.topic.data, 
			author=current_user, 
			body=form.body.data, 
			time_end=form.time_end.data)
		db.session.add(todo)
		db.session.commit()
		flash('Ваше событие зарегистрировано!')
		return redirect(url_for('index'))
	return render_template('user.html', user=user, todos=todos, form=form)

@app.route('/todos')
@login_required
def todos():
	todos = Todo.query.order_by(Todo.created_at).all()
	return render_template('todos.html', todos=todos)

@app.route('/todos/<int:id>')
@login_required
def todo(id):
	todo = Todo.query.filter_by(id=id).first()
	return render_template('todo.html', todo=todo)

@app.route('/todos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def change_todo(id):
	todo = Todo.query.filter_by(id=id).first()
	form = TodoForm()
	if current_user.username == todo.author.username:
		if request.method == "POST":
			if todo.topic:
				todo.topic = form.topic.data
			todo.body = form.body.data
			todo.time_end = form.time_end.data
			db.session.add(todo)
			db.session.commit()
			return redirect(f'/todos/{id}')
		if todo:
			form.topic.data = todo.topic
			form.body.data = todo.body
			form.time_end.data = todo.time_end
			return render_template('change_todo.html', form=form, todo=todo)
	return redirect(url_for(f'todos'))

@app.route('/todo_delete/<int:id>')
@login_required
def delete_todo(id):
	todo = Todo.query.filter_by(id=id).first()
	db.session.delete(todo)
	db.session.commit()
	flash(f'{todo.author.username} вы успешно удалили свою запись!')
	return redirect(url_for('todos'))