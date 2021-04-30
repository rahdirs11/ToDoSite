from flask import render_template, request, redirect, url_for, flash, session
from todo.models import Users, Lists, Tasks, Admins
from todo.forms import RegistrationForm, LoginForm, AddListForm, AddTaskForm, RenameTaskForm, RenameListForm, AdminLoginForm
from todo import app, bcrypt, db, bootstrap
from datetime import datetime, timedelta
# from flask_login import login_user, current_user, logout_user

@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html', title="HOME", home=True)


@app.route('/admin', methods=['POST', 'GET'])
def adminLogin():
	if session.get('admin', None):
		return redirect(url_for('adminDashboard'))

	form = AdminLoginForm()
	if form.validate_on_submit():
		admin = Admins.query.filter_by(email=form.email.data).first()
		if admin and bcrypt.check_password_hash(admin.password, form.password.data):
			session['admin'] = admin.email
			flash(f'Admin - {admin.lastName}, {admin.firstName} has successfully logged in!', 'success')
			return redirect(url_for('adminDashboard'))
	return render_template('adminLogin.html', form=form, adminLogin=True)


@app.route('/admin/dashboard', methods=['GET', 'POST'])
def adminDashboard():
	users = Users.query.all()
	users24 = db.session.query(Users).filter(signupTime >= datetime.now() - timedelta(hours=24)).all()
	lists = Lists.query.all()
	lists24 = db.session.query(Lists).filter(creationTime >= datetime.now() - timedelta(hours=24)).all()
	details = {
		'totalSignups': len(users),
		'totalSignups24': len(users24),
		'totalLists': len(lists),
		'totalLists24': len(lists24),
	}
	return render_template('adminDashboard.html', adminDashboard=True, details=details)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated():
    #     return redirect(url_for('dashboard'))
    if session.get('username', None):
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, password=hashed, firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form, register=True)


@app.route('/login', methods=['POST', 'GET'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))
    if session.get('username', None):
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        # check if the entered email (from the form) exists in the database
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login_user(user)
            session['username'] = user.username
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful: Invalid email and/or password!', 'danger')
            return render_template('login.html', title="Login", form=form, signup=True)
    return render_template('login.html', title="Login", login=True, form=form, signup=False)


@app.route('/logout')
def logout():
	if session.get('username', None):
		user = Users.query.filter_by(username=session.get('username')).first()
		user.logoutTime =
		flash(f'{session.get("username")}, you have been logged out', 'info')

	if session.get('admin', None):
		admin = Admins.query.filter_by(email=session.get("admin")).first()
		flash(f'Admin - {admin.Id}, you have been logged out', 'info')

	session.pop('admin', None)
	session.pop('username', None)
	return redirect(url_for('home'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # should be able to select existing list or create new list
	# if a list is visited, all the tasts in that list must be listed
	# the tasks in every list can be deleted, marked as done, or renamed
    currentUser = Users.query.filter_by(username=session.get('username')).first()
    # listOfTasks = Lists.query.filter_by(uid=currentUser.Id).first()
    # print(currentUser.username)
    tasks = []
    if len(currentUser.lists) == 0:
        tasks = []
    else:
        tasks = currentUser.lists
    addList = AddListForm()
    if addList.validate_on_submit():
        # print(f'Type of currentUser.Id: {type(currentUser.Id)}\naddList.List = {addList.List}')
        currList = Lists(name=addList.List.data, uid=int(currentUser.Id))
        db.session.add(currList)
        db.session.commit()
        flash('A new list was added to your to-do manager!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', title="Dashboard", dashboard=True, lists=tasks, form=addList, displayList=True, displayTask=False)


@app.route('/lists/delete/<int:lid>', methods=['GET', 'POST'])
def deleteList(lid):
	lists = Users.query.filter_by(username=session.get('username', None)).first().lists
	if lid in range(1, len(lists) + 1):
		toBeDeleted = Lists.query.filter_by(Id=lists[lid - 1].Id).first()
		db.session.delete(toBeDeleted)
		db.session.commit()
		flash(f'Successfully deleted List {toBeDeleted.name[: 4]}......', 'success')
	else:   flash(f'Please choose a valid list number!', 'danger')
	return redirect(url_for('dashboard'))


@app.route('/lists/rename/<int:lid>', methods=['GET', 'POST'])
def renameList(lid):
    form = RenameListForm()
    if form.validate_on_submit():
        l = Users.query.filter_by(username=session.get('username')).first().lists[lid - 1]
        l.name = form.newListName.data
        db.session.commit()
        flash(f'Successfully renamed List #{lid}', 'success')
        return redirect(url_for('dashboard'))
    return render_template('renameList.html', form=form, title="Rename List")


@app.route('/tasks/add/<int:ID>', methods=['POST', 'GET'])
def addTask(ID):
	form = AddTaskForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			l = Users.query.filter_by(username=session.get('username')).first().lists[ID - 1]
			task = Tasks(taskName=form.task.data, tid=l.Id)
			flash(f'Added a new task to List {task.taskName[: 4]}...', 'success')
			db.session.add(task)
			db.session.commit()
			return redirect(url_for('dashboard'))
	return render_template('addTask.html', title="Add Task", form=form)


@app.route('/tasks/rename/<int:lid>/<int:tid>', methods=['POST', 'GET'])
def renameTask(lid, tid):
    form = RenameTaskForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            lists = Users.query.filter_by(username=session.get('username')).first().lists[lid - 1]
            task = lists.tasks[tid - 1]
            task.taskName = form.newTaskName.data
            db.session.commit()
            flash(f'Renamed Task#{tid} in List#{lid}', 'success')

            return redirect(url_for('dashboard'))
    return render_template('renameTask.html', title="Rename Task", form=form)


@app.route('/tasks/delete/<int:lid>/<int:tid>', methods=['POST', 'GET'] )
def deleteTask(lid, tid):
    tasks = Users.query.filter_by(username=session['username']).first().lists[lid - 1].tasks
    taskTBD = tasks[tid - 1]
    db.session.delete(taskTBD)
    db.session.commit()
    flash(f'Deleted Task#{tid} from List#{lid}', 'danger')
    return redirect(url_for('dashboard'))


@app.route('/tasks/changeStatus/<int:lid>/<int:tid>', methods=['POST', 'GET'])
def changeStatus(lid, tid):
    tasks = Users.query.filter_by(username=session['username']).first().lists[lid - 1].tasks
    task = tasks[tid - 1]
    task.status = not task.status
    db.session.commit()
    flash(f'You have completed Task#{tid}!!!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = Users.query.filter_by(username=session['username']).first()
    return render_template('profile.html', user=user)
