import sys
sys.path.append('../../')

from mainapp.models.models import Appointment
from mainapp.utils import utils
from mainapp.services import appointmentservice as app_repository
from flask import Blueprint,request, jsonify, abort


rest_end_point_bp = Blueprint('rest_end_point_bp',__name__)


@rest_end_point_bp.route('/',methods=["POST"])
def create_appointment():
    """
    validates incoming json data and saves
    """
    if not request.json :
        abort(400)
    if not 'appointment_time' in request.json:
        abort(400)
    if not 'description' in request.json:
        abort(400)

    appointment = Appointment(None,
                    utils.format_date(request.json['appointment_time']),
                    request.json['description'])

    app_repository.add_appointment(appointment)
    return jsonify({'message':'Appointment Saved !'}), 200


@rest_end_point_bp.route('/',methods=['GET'])
def get_all():
    """
    returns all appointments
    """
    appointments = app_repository.get_all_appointments()

    return jsonify([appointment.serialize() for appointment in appointments]) \
            if appointments !=[] else \
            jsonify({"message":"No appointments made !"})

@rest_end_point_bp.route('/<string:keyword>',methods=['GET'])
def get_by_description(keyword):
    """
    returns all appointments containing keyword
    @param keyword
    """
    appointments = app_repository.find_by_description(keyword)
    return jsonify([appointment.serialize() for appointment in appointments]) \
            if appointments !=[] else \
            jsonify({"message":"No appointments made !"})
