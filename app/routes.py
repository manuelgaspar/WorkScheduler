from app import WorkScheduler, db
from app.forms import LoginForm, RegistrationForm, TaskForm
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Task
from werkzeug.urls import url_parse
from datetime import datetime

@WorkScheduler.route('/')
@WorkScheduler.route('/index')
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    tasks = []
    for task in user.tasks:
        if task.date == datetime.today().date():
            tasks.append(task)
    return render_template('index.html', title='Home', tasks=tasks)

@WorkScheduler.route('/login', methods=['GET', 'POST'])
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
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@WorkScheduler.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@WorkScheduler.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registration successful')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@WorkScheduler.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username)
        task = Task(body=form.body.data, date=form.date.data, time=form.time.data, recurrent=form.recurrent.data, email_alert=form.alert.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task creation successful')
        return redirect(url_for('index'))
    return render_template('new_task.html', title='New Task', form=form)

@WorkScheduler.route('/cenas')
def cenas():
	return render_template('calendar_view_2.html')

@WorkScheduler.route('/calendar_events')
def calendar_events(start_date, end_date):
    resp = jsonify({'success' : 1, 'result' : []})
    resp.status_code = 200
    print(resp)
    print('cenas e coisas')
    return resp

@WorkScheduler.route('/cenas_2')
def cenas_2():
	return render_template('new_calendar_view.html')

# https://www.reddit.com/r/learnpython/comments/90otn8/how_to_add_and_display_events_using_my_python/
# https://codepen.io/peanav/pen/ulkof
# https://codepen.io/SamMarkiewicz/pen/xjmEr
# https://www.reddit.com/r/flask/comments/7zzbkd/calendar/
# https://github.com/sukeesh/flask-calendar
# https://www.reddit.com/r/learnpython/comments/2lk6lj/how_to_implement_a_web_calendar/