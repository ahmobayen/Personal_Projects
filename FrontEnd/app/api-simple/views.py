<<<<<<< HEAD
from flask import render_template, Response, jsonify
from flask_login import login_required, current_user

from . import api

from ..socket_client_side import simple_receive, video_receive


@api.route('/video_history')
@login_required
def json():
    """
    Render the dashboard template on the /dashboard route
    """
    try:
        return str(simple_receive().decode('utf-8'))
    except ConnectionError:
        return '', 502


@api.route('/video_feedback')
@login_required
def video_feed():
    try:
        return Response(video_receive(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except ConnectionError:
=======
from flask import render_template, Response, jsonify
from flask_login import login_required, current_user

from . import api

from ..socket_client_side import simple_receive, video_receive


@api.route('/video_history')
@login_required
def json():
    """
    Render the dashboard template on the /dashboard route
    """
    try:
        return str(simple_receive().decode('utf-8'))
    except ConnectionError:
        return '', 502


@api.route('/video_feedback')
@login_required
def video_feed():
    try:
        return Response(video_receive(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except ConnectionError:
>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
        return '', 502