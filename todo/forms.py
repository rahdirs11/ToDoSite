from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from todo.models import Users, Lists, Tasks
from todo import db
from flask import session


# form to sign up
class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	username = StringField('Username', validators=[DataRequired(), Length(min=4, max=30)])
	firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
	lastName = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=30)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
	confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Signup')


	def validate_username(self, username):
		user = Users.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username unavailable! Please use a different one')


	def validate_email(self, email):
		user = Users.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Username already taken! Try a different one!')

# form for loggin in
class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	login = SubmitField('LogIn')

# form to add a new list
class AddListForm(FlaskForm):
	add = SubmitField('Add List')
	List = StringField(validators=[DataRequired(), Length(min=5)])

	# checking if the list already exists
	def validate_List(self, List):
		userLists = Users.query.filter_by(username=session['username']).first().lists
		# print(f'Current User id: {user.Id}')
		# print(userLists, List.data, sep="\n")
		for l in userLists:
			if l.name.lower() == List.data.lower():
				raise ValidationError('The list already exists!')


class AddTaskForm(FlaskForm):
	add = SubmitField('Add Task')
	task = StringField(validators=[DataRequired(), Length(min=5)])

	# checking if the list already exists
	def validate_task(self, task):
		pass


class RenameTaskForm(FlaskForm):
	newTaskName = StringField('New Task Name', validators=[DataRequired()])
	rename = SubmitField('Rename Task')
	def validate_newTaskName(self, newTask):
		pass


class RenameListForm(FlaskForm):
	newListName = StringField('New Task Name', validators=[DataRequired()])
	rename = SubmitField('Rename List')


class AdminLoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	login = SubmitField('Login')
