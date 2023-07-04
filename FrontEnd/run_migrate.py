<<<<<<< HEAD
def run_migrate():
    import os
    if os.path.exists('migrations'):
        pass
    else:
        for commands in ['init', 'migrate', 'upgrade']:
            os.system('flask db {command}'.format(command=commands))


def create_admin():
    from run import app
    from app import db
    from app.models import User, Group, Role, UserRole, UserGroup
    app.app_context().push()

    # define roles:
    role_admin = Role(name='administrator', description=' Highest privilege access',
                      permission_create=True, permission_update=True, permission_read=True, permission_delete=True)
    role_power_user = Role(name='power_user', description=' moderate privilege access', permission_create=True,
                           permission_update=True, permission_read=True, permission_delete=False)
    role_user = Role(name='normal_user', description=' lowest privilege access', permission_create=False,
                     permission_update=False, permission_read=True, permission_delete=False)

    # define groups:
    group_managers = Group(name='managers', description='Highest privilege access',
                           access_dashboard=True, access_api=True, access_setting=True)

    group_developers = Group(name='developers', description='moderate privilege access to api and dashboards',
                             access_dashboard=True, access_api=True, access_setting=False)

    group_analyzers = Group(name='analyzers', description='minimum privilege access. Only to dashboards',
                            access_dashboard=True, access_api=False, access_setting=False)

    group_api_only = Group(name='api_access', description='minimum privilege access. only to API',
                           access_dashboard=False, access_api=True, access_setting=False)

    # define admin access:
    admin = User(username='admin', first_name='AmirHossein', last_name='Mobayen',
                 email='a.h.mobayen@gmail.com', password="123QWEasdzxc", is_admin=True)
    assign_admin_role = UserRole(user_id='1', role_id='1')
    assign_admin_group = UserGroup(user_id='1', group_id='1')

    init_db_values = [role_admin, role_power_user, role_user,
                      group_managers, group_developers, group_analyzers, group_api_only,
                      admin, assign_admin_role, assign_admin_group]
    db.session.add_all(init_db_values)
    db.session.commit()


if __name__ == '__main__':
    run_migrate()
    create_admin()


=======
def run_migrate():
    import os
    if os.path.exists('migrations'):
        pass
    else:
        for commands in ['init', 'migrate', 'upgrade']:
            os.system('flask db {command}'.format(command=commands))


def create_admin():
    from run import app
    from app import db
    from app.models import User, Group, Role, UserRole, UserGroup
    app.app_context().push()

    # define roles:
    role_admin = Role(name='administrator', description=' Highest privilege access',
                      permission_create=True, permission_update=True, permission_read=True, permission_delete=True)
    role_power_user = Role(name='power_user', description=' moderate privilege access', permission_create=True,
                           permission_update=True, permission_read=True, permission_delete=False)
    role_user = Role(name='normal_user', description=' lowest privilege access', permission_create=False,
                     permission_update=False, permission_read=True, permission_delete=False)

    # define groups:
    group_managers = Group(name='managers', description='Highest privilege access',
                           access_dashboard=True, access_api=True, access_setting=True)

    group_developers = Group(name='developers', description='moderate privilege access to api and dashboards',
                             access_dashboard=True, access_api=True, access_setting=False)

    group_analyzers = Group(name='analyzers', description='minimum privilege access. Only to dashboards',
                            access_dashboard=True, access_api=False, access_setting=False)

    group_api_only = Group(name='api_access', description='minimum privilege access. only to API',
                           access_dashboard=False, access_api=True, access_setting=False)

    # define admin access:
    admin = User(username='admin', first_name='AmirHossein', last_name='Mobayen',
                 email='a.h.mobayen@gmail.com', password="123QWEasdzxc", is_admin=True)
    assign_admin_role = UserRole(user_id='1', role_id='1')
    assign_admin_group = UserGroup(user_id='1', group_id='1')

    init_db_values = [role_admin, role_power_user, role_user,
                      group_managers, group_developers, group_analyzers, group_api_only,
                      admin, assign_admin_role, assign_admin_group]
    db.session.add_all(init_db_values)
    db.session.commit()


if __name__ == '__main__':
    run_migrate()
    create_admin()


>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
