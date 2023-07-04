<<<<<<< HEAD
# application/home/views.py

from flask import render_template, Response, abort
from flask_login import login_required, current_user
from . import home
import ast

from ..socket_client_side import simple_receive, video_receive


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    try:
        table_data = simple_receive().decode('utf-8')
        table_data = ast.literal_eval(table_data[1:-1])
    except ConnectionRefusedError as error:
        table_data = {}
    finally:
        return render_template('home/dashboard.html', title="Dashboard", table_output=table_data)


@home.route('/video_feed')
@login_required
def video_feed():
    try:
        return Response(video_receive(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except ConnectionError:
        return render_template('errors/502.html', title="image")

=======
# application/home/views.py

from flask import render_template, Response, abort
from flask_login import login_required, current_user
from . import home
import ast

from ..socket_client_side import simple_receive, video_receive


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    try:
        table_data = simple_receive().decode('utf-8')
        table_data = ast.literal_eval(table_data[1:-1])
    except ConnectionRefusedError as error:
        table_data = {}
    finally:
        return render_template('home/dashboard.html', title="Dashboard", table_output=table_data)


@home.route('/video_feed')
@login_required
def video_feed():
    try:
        return Response(video_receive(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except ConnectionError:
        return render_template('errors/502.html', title="image")

>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
