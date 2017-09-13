import sys
sys.path.append('../../')

from mainapp.blueprints import mainappbp
from mainapp.models.models import Appointment
from mainapp.utils import utils
from flask import g,current_app

import time

__tbl_name__ = "tbl_appointments"

def add_appointment(appointment):
    """
    Adds appointment object to database
    @param Appointment
    """
    try:
        db = mainappbp.get_db(current_app)
        cursor = db.cursor()
        cursor.execute('INSERT INTO '+__tbl_name__
                        +'(appointment_time,description) VALUES (?, ?)',
                        list(
                        [appointment.appointment_time,appointment.description]
                        )
                    )
                    
        db.commit()
    except:
        if mainappbp.get_db(current_app)==None:
            raise RuntimeError("No db connection")
        if appointment.appointment_time == None or appointment.description == None :
            raise ValueError("Both attributes of appointment cannot be null")


def get_all_appointments():
    """
    Returns appointment object in DB.
    """
    db = mainappbp.get_db(current_app)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM '+ __tbl_name__)
    result_set = cursor.fetchall()
    return [Appointment(result[0],utils.format_date(result[1]),result[2]) for result in result_set]

def find_by_description(keyword):
    """
    Returns list of appointment objects selectively.
    @param keyword
    """
    db = mainappbp.get_db(current_app)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM "+ __tbl_name__+" WHERE  instr(description,?)",(keyword,))
    result_set = cursor.fetchall()
    return [Appointment(result[0],utils.format_date(result[1]),result[2]) for result in result_set]
