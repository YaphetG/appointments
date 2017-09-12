import sys
sys.path.append('../../')

from mainapp.blueprints import mainappbp
from flask import g,current_app

__tbl_name__ = "tbl_appointments"

def add_appointment(appointment):
    try:
        db = mainappbp.get_db(current_app)
        cursor = db.cursor()
        cursor.execute('INSERT INTO '+__tbl_name__+'(appointment_time,description) VALUES (?, ?)',list([appointment.appointment_time,appointment.description]))
        db.commit()
    except:
        if mainappbp.get_db(current_app)==None:
            raise RuntimeError("No db connection")
        if appointment.appointment_time == None or appointment.description == None :
            raise ValueError("Both attributes of appointment cannot be null")
