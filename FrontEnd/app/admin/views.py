<<<<<<< HEAD
# application/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .. import db

from .forms import GroupForm, RoleForm, UserAssignForm
from ..models import Group, Role, User, Setting, UserGroup, UserRole


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Group Views
@admin.route('/groups', methods=['GET', 'POST'])
@login_required
def list_groups():
    """
    List all groups
    """
    check_admin()

    groups = Group.query.all()

    return render_template('admin/groups/groups.html',
                           groups=groups, title="Groups")


@admin.route('/groups/add', methods=['GET', 'POST'])
@login_required
def add_group():
    """
    Add a group to the database
    """
    check_admin()

    add_group = True

    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data,
                      description=form.description.data)
        try:
            # add group to the database
            db.session.add(group)
            db.session.commit()
            flash('You have successfully added a new group.')
        except:
            # in case group name already exists
            flash('Error: group name already exists.')

        # redirect to groups page
        return redirect(url_for('admin.list_groups'))

    # load group template
    return render_template('admin/groups/group.html', action="Add",
                           add_group=add_group, form=form,
                           title="Add Group")


@admin.route('/groups/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_group(id):
    """
    Edit a group
    """
    check_admin()

    add_group = False

    group = Group.query.get_or_404(id)
    form = Group(obj=group)
    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the group.')

        # redirect to the groups page
        return redirect(url_for('admin.list_groups'))

    form.description.data = group.description
    form.name.data = group.name
    return render_template('admin/groups/group.html', action="Edit",
                           add_group=add_group, form=form,
                           group=group, title="Edit Group")


@admin.route('/groups/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_group(id):
    """
    Delete a group from the database
    """
    check_admin()

    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    flash('You have successfully deleted the group.')

    # redirect to the groups page
    return redirect(url_for('admin.list_groups'))

    return render_template(title="Delete Groups")


# Role Views
@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# User Views
@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = db.session.query(User.id, User.first_name, User.last_name,
                             Group.name.label('group_name'), Role.name.label('role_name'))\
        .filter(User.id == UserGroup.user_id).filter(UserGroup.group_id == Group.id)\
        .filter(User.id == UserRole.user_id).filter(UserRole.role_id == Role.id)

    # users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign a group and a role to an user
    """
    check_admin()

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a group or role
    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        group = form.group.data
        role = form.role.data
        user_group = UserGroup.query.filter_by(user_id=id).first()
        user_role = UserRole.query.filter_by(user_id=id).first()

        if user_group:
            db.session.delete(user_group)
            db.session.commit()

        if user_role:
            db.session.delete(user_role)
            db.session.commit()

        db.session.add(UserGroup(user_id=user.id, group_id=group.id))
        db.session.add(UserRole(user_id=user.id, role_id=role.id))
        db.session.commit()

        flash('You have successfully assigned a group and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')


@admin.route('/settings')
@login_required
def list_settings():
    """
    Setting Controlling
    """
    check_admin()

    settings = Setting.query.all()
    return render_template('admin/settings/settings.html',
                           settings=settings, title='Settings')


@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    delete existing User
    """
    check_admin()

    user = User.query.get_or_404(id)
    user_group = UserGroup.query.filter_by(user_id=id).first()
    user_role = UserRole.query.filter_by(user_id=id).first()

    # prevent deleting admin users
    if not user.is_admin:
        for delete_query in [user, user_group, user_role]:
            db.session.delete(delete_query)
        db.session.commit()
        flash('{display_user} have successfully removed.'.format(display_user=user.username))

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))
    else:
        abort(403)

    # return render_template('admin/users/user.html', user=user, form=form, title='Delete User')
=======
# application/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .. import db

from .forms import GroupForm, RoleForm, UserAssignForm
from ..models import Group, Role, User, Setting, UserGroup, UserRole


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Group Views
@admin.route('/groups', methods=['GET', 'POST'])
@login_required
def list_groups():
    """
    List all groups
    """
    check_admin()

    groups = Group.query.all()

    return render_template('admin/groups/groups.html',
                           groups=groups, title="Groups")


@admin.route('/groups/add', methods=['GET', 'POST'])
@login_required
def add_group():
    """
    Add a group to the database
    """
    check_admin()

    add_group = True

    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data,
                      description=form.description.data)
        try:
            # add group to the database
            db.session.add(group)
            db.session.commit()
            flash('You have successfully added a new group.')
        except:
            # in case group name already exists
            flash('Error: group name already exists.')

        # redirect to groups page
        return redirect(url_for('admin.list_groups'))

    # load group template
    return render_template('admin/groups/group.html', action="Add",
                           add_group=add_group, form=form,
                           title="Add Group")


@admin.route('/groups/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_group(id):
    """
    Edit a group
    """
    check_admin()

    add_group = False

    group = Group.query.get_or_404(id)
    form = Group(obj=group)
    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the group.')

        # redirect to the groups page
        return redirect(url_for('admin.list_groups'))

    form.description.data = group.description
    form.name.data = group.name
    return render_template('admin/groups/group.html', action="Edit",
                           add_group=add_group, form=form,
                           group=group, title="Edit Group")


@admin.route('/groups/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_group(id):
    """
    Delete a group from the database
    """
    check_admin()

    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    flash('You have successfully deleted the group.')

    # redirect to the groups page
    return redirect(url_for('admin.list_groups'))

    return render_template(title="Delete Groups")


# Role Views
@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# User Views
@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = db.session.query(User.id, User.first_name, User.last_name,
                             Group.name.label('group_name'), Role.name.label('role_name'))\
        .filter(User.id == UserGroup.user_id).filter(UserGroup.group_id == Group.id)\
        .filter(User.id == UserRole.user_id).filter(UserRole.role_id == Role.id)

    # users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign a group and a role to an user
    """
    check_admin()

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a group or role
    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        group = form.group.data
        role = form.role.data
        user_group = UserGroup.query.filter_by(user_id=id).first()
        user_role = UserRole.query.filter_by(user_id=id).first()

        if user_group:
            db.session.delete(user_group)
            db.session.commit()

        if user_role:
            db.session.delete(user_role)
            db.session.commit()

        db.session.add(UserGroup(user_id=user.id, group_id=group.id))
        db.session.add(UserRole(user_id=user.id, role_id=role.id))
        db.session.commit()

        flash('You have successfully assigned a group and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')


@admin.route('/settings')
@login_required
def list_settings():
    """
    Setting Controlling
    """
    check_admin()

    settings = Setting.query.all()
    return render_template('admin/settings/settings.html',
                           settings=settings, title='Settings')


@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    delete existing User
    """
    check_admin()

    user = User.query.get_or_404(id)
    user_group = UserGroup.query.filter_by(user_id=id).first()
    user_role = UserRole.query.filter_by(user_id=id).first()

    # prevent deleting admin users
    if not user.is_admin:
        for delete_query in [user, user_group, user_role]:
            db.session.delete(delete_query)
        db.session.commit()
        flash('{display_user} have successfully removed.'.format(display_user=user.username))

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))
    else:
        abort(403)

    # return render_template('admin/users/user.html', user=user, form=form, title='Delete User')
>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
