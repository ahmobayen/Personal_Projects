<<<<<<< HEAD

from flask_login import login_required
from flask_restx import Namespace, Resource, fields


api = Namespace('slots', description='Showing Parking Slots Status')

slot = api.model('Slots',
                 {
                     'id': fields.String(required=False, description='The Slot identifier'),
                     'status': fields.String(required=False, description='Returns slot status as boolean'),
                     'time': fields.String(required=False, description='Date and time that slot is checked')
                 })

SLOT_EXAMPLE = [
    {'id': 5, 'status': 1, 'time': '2020-01-01 05:05:05'},
    {'id': 2, 'status': 0, 'time': '2020-01-01 05:05:05'},
    {'id': 3, 'status': 1, 'time': '2020-01-01 05:05:05'}
]


@api.route('/')
# @api.doc(params={'id': 'An Id', 'Name': 'String'})
class SlotStatusList(Resource):
    @api.doc('slots_list')
    @api.marshal_list_with(slot)
    def get(self):
        return SLOT_EXAMPLE
=======

from flask_login import login_required
from flask_restx import Namespace, Resource, fields


api = Namespace('slots', description='Showing Parking Slots Status')

slot = api.model('Slots',
                 {
                     'id': fields.String(required=False, description='The Slot identifier'),
                     'status': fields.String(required=False, description='Returns slot status as boolean'),
                     'time': fields.String(required=False, description='Date and time that slot is checked')
                 })

SLOT_EXAMPLE = [
    {'id': 5, 'status': 1, 'time': '2020-01-01 05:05:05'},
    {'id': 2, 'status': 0, 'time': '2020-01-01 05:05:05'},
    {'id': 3, 'status': 1, 'time': '2020-01-01 05:05:05'}
]


@api.route('/')
# @api.doc(params={'id': 'An Id', 'Name': 'String'})
class SlotStatusList(Resource):
    @api.doc('slots_list')
    @api.marshal_list_with(slot)
    def get(self):
        return SLOT_EXAMPLE
>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
