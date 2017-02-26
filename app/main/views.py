from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import Permission, Role, User2, Student, Subject, Performance
from ..decorators import admin_required, permission_required



def addSubjects():
    for index in range(40):
        subject = Subject(name=("Subject"+ str(index)), major="Electronics",
                          description="Blah blah")
        db.session.add(subject)
    db.session.commit()

def addPerformance():
    sub = Subject.query.filter_by(name=("Subject"+str(0))).first()
    for index in range(4):
        perf = Performance(semester=index, student_id=current_user.student_id,
                           subject_id=sub.id,
                           teachername="John Doe", exam_id=index, grade=45.6,
                           remarks="none")
        db.session.add(perf)
    db.session.commit()

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():

    if not current_user.is_anonymous:
        print "Current user student id"
        print current_user.student_id
        student = Student.query.get(current_user.student_id)
        return render_template('index.html', student=student)
    else:
        return render_template('index.html')



@main.route('/user/<username>')
@login_required
def user(username):
    user = User2.query.filter_by(username=username).first_or_404()
    student = Student.query.get(user.student_id)
    info = []
    info.append(45)
    info.append(35)
    info.append(45)
    info.append(40)
    return render_template('user.html', user=user, student=student, info=info )


@main.route('/generatedata')
@login_required
def generatedata():
    flash('Generating data')
    addSubjects()
    addPerformance()
    return redirect(url_for('.index'))



@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


