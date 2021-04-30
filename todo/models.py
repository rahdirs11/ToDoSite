from todo import db
from datetime import datetime
# from flask_login import UserMixin


# @loginManager.user_loader
# def loadUser(userID):
#     return Users.query.get(int(userID))

class Admins(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return 'Admin<{}>'.format(self.email)

# Users Table -> containing all registered users who can later sign in
class Users(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    lists = db.relationship('Lists', backref='username', lazy=True, cascade='all')
    loginTime = db.Column(db.DateTime, default=datetime.now())
    logoutTime = db.Column(db.DateTime)
    signupTime = db.Column(db.DateTime)

    def __repr__(self):
        return f'User("{self.email}", "{self.lastName}, {self.firstName}", "{self.username}")'


# Lists Table -> contains a table of lists for all users
class Lists(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Tasks', backref='listName', lazy=True, cascade="all")
    uid = db.Column(db.Integer, db.ForeignKey('users.Id', ondelete="CASCADE"), nullable=False)
    creationTime = db.Column(db.DateTime, default=datetime.now())


    def __repr__(self):
        return f'{self.name}: User: {self.username.username}'
    # include foreign key linking to Users



# Tasks Table -> contains a table of tasks under each list, for all users
class Tasks(db.Model):
	Id = db.Column(db.Integer, primary_key=True)
	taskName = db.Column(db.String(100), nullable=False, unique=True)
	status = db.Column(db.Boolean, default=False)
	tid = db.Column(db.Integer, db.ForeignKey('lists.Id', ondelete='CASCADE'), nullable=False)
