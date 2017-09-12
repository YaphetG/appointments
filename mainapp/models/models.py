
class Appointment:

    def __init__(self,id,appointment_time,description):
        """
        constructor for Appointment model
        @param appointment_time datetime type
        @param description with max length 255
        """
        self.appointment_time = appointment_time
        self.description = description
