import sys
sys.path.append('../')
import os
import tempfile

import time
import unittest

from mainapp import run as bootstrap
from mainapp.blueprints import mainappbp
from mainapp.config.config import TestingConfig
from flask import g
from mainapp.services import appointmentservice as service
from mainapp.models.models import Appointment
import datetime
class ServicesTestCase(unittest.TestCase):
    def setUp(self):
        #set up test with temp db file
        self.app = bootstrap.create_app(TestingConfig)
        #override with testing config
        self.app.config.from_object(TestingConfig)
        self.file_handle , self.app.config['DATABASE'] = tempfile.mkstemp()
        self.app.testing = True
        self.test_client =self.app.test_client()
        with self.app.app_context():
            mainappbp.init_db(self.app)


    def tearDown(self):
        os.close(self.file_handle)
        os.unlink(self.app.config['DATABASE'])

    def test_add_appointment_happyday(self):
        with self.app.app_context():
            db =  mainappbp.get_db(self.app)

            date = datetime.datetime(2017,10,21,12,00)
            appointment = Appointment(None,date,"Birthday")
            service.add_appointment(appointment)

            cursor = db.cursor()
            result = cursor.execute("SELECT * from tbl_appointments").fetchone()
            assert result[0] == 1
            # '2017-10-21 12:00:00'
            assert result[1] == date.strftime('%Y-%m-%d %H:%M:%S')

            assert result[2] == "Birthday"


    def test_add_appointment_exception_no_context(self):
        date = datetime.datetime(2017,10,21,12,00)
        self.assertRaises(RuntimeError,service.add_appointment,Appointment(None,date,"desc"))

    def test_add_appointment_with_null(self):
        with self.app.app_context():
            appointment = Appointment(None,None,None)
            self.assertRaises(ValueError,service.add_appointment,appointment)



    def test_get_appointment_with_values(self):
        with self.app.app_context():
            db =  mainappbp.get_db(self.app)
            cursor = db.cursor()
            query = """INSERT INTO tbl_appointments (appointment_time, description ) VALUES
                ('2017-09-13 08:08:00','inserting data'),
                ('2017-09-13 08:08:30','another appointment')
                """
            cursor.execute(query)

            expected = [{
                'id' : 1,
                'time': time.strptime('2017-09-13 08:08:00','%Y-%m-%d %H:%M:%S'),
                'desc': 'inserting data'
                },
                {
                'id' : 2,
                'time': time.strptime('2017-09-13 08:08:30','%Y-%m-%d %H:%M:%S'),
                'desc': 'another appointment'
                }
                ]
            db.commit()
            #should return all the rows converted to appointments model
            result_set = service.get_all_appointments()
            i=0
            for ex,result in map(expected,result_set):
                assert ex.id == result.id
                assert ex.time == result.appointment_time
                assert ex.desc == result.description


    def test_get_appointment_empty(self):
        pass

if __name__ == '__main__':
    unittest.main()
