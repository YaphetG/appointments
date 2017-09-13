import sys
sys.path.append('../../')
from mainapp.utils import utils
import datetime
class Appointment:

    def __init__(self,id,appointment_time,description):
        """
        constructor for Appointment model
        @param appointment_time datetime type
        @param description with max length 255
        """
        self.id = id
        self.appointment_time = appointment_time
        self.description = description

    def serialize(self):
        return {
            'id' : str(self.id),
            'appointment_time' : self.appointment_time.strftime(utils.SQL_DATE_TIME_FORMAT),
            'description' : self.description
        }
