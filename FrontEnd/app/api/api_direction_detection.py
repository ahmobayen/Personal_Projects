<<<<<<< HEAD
from ast import literal_eval

from flask_login import login_required
from flask_restx import Namespace, Resource, fields

from app.socket_client_side import simple_receive

api = Namespace('history', description='Browsing history of detected objects')

history = api.model('History',
                    {
                        'id': fields.String(required=False, description='The Object identifier'),
                        'name': fields.String(required=False, description='Detected object name'),
                        'direction': fields.String(required=False, description='movement direction of detected object'),
                        'time': fields.String(required=False, description='Date and time that object is detected')
                    })


@api.route('/')
# @api.doc(params={'id': 'An Id', 'Name': 'String'})
class DetectedObjectList(Resource):
    @api.doc('history_list')
    @api.marshal_list_with(history)
    def get(self):
        return literal_eval(str(simple_receive().decode('utf-8')))



=======
from ast import literal_eval

from flask_login import login_required
from flask_restx import Namespace, Resource, fields

from app.socket_client_side import simple_receive

api = Namespace('history', description='Browsing history of detected objects')

history = api.model('History',
                    {
                        'id': fields.String(required=False, description='The Object identifier'),
                        'name': fields.String(required=False, description='Detected object name'),
                        'direction': fields.String(required=False, description='movement direction of detected object'),
                        'time': fields.String(required=False, description='Date and time that object is detected')
                    })


@api.route('/')
# @api.doc(params={'id': 'An Id', 'Name': 'String'})
class DetectedObjectList(Resource):
    @api.doc('history_list')
    @api.marshal_list_with(history)
    def get(self):
        return literal_eval(str(simple_receive().decode('utf-8')))



>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
