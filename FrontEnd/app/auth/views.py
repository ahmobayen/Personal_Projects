<<<<<<< HEAD
# application/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User, UserGroup, UserRole, Role, Group


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    username=form.username.data, password=form.password.data)
        db.session.add(user)

        group = Group.query.filter_by(name='analyzers').first()
        role = Role.query.filter_by(name='normal_user').first()
        user_group = UserGroup(user_id=user.id, group_id=group.id)
        user_role = UserRole(user_id=user.id, role_id=role.id)

        # add user to the database
        for query in [user_role, user_group]:
            db.session.add(query)

        db.session.commit()

        flash('{display_user} have successfully registered!'.format(display_user=user.username))

        # redirect to the login page
        return redirect(url_for('admin.list_users'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log user in
            login_user(user)

            # redirect to the appropriate dashboard page
            return redirect(url_for('home.dashboard'))
        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
=======
# application/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User, UserGroup, UserRole, Role, Group


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    username=form.username.data, password=form.password.data)
        db.session.add(user)

        group = Group.query.filter_by(name='analyzers').first()
        role = Role.query.filter_by(name='normal_user').first()
        user_group = UserGroup(user_id=user.id, group_id=group.id)
        user_role = UserRole(user_id=user.id, role_id=role.id)

        # add user to the database
        for query in [user_role, user_group]:
            db.session.add(query)

        db.session.commit()

        flash('{display_user} have successfully registered!'.format(display_user=user.username))

        # redirect to the login page
        return redirect(url_for('admin.list_users'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log user in
            login_user(user)

            # redirect to the appropriate dashboard page
            return redirect(url_for('home.dashboard'))
        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
    return redirect(url_for('auth.login'))