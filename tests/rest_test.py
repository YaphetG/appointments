import sys
sys.path.append('../')

import unittest
import os
import tempfile

from flask import json, jsonify
from mainapp import run as bootstrap
from mainapp.config.config import TestingConfig
from mainapp.utils import utils
from mainapp.models.models import Appointment
from mainapp.blueprints import mainappbp


class RestTestCase(unittest.TestCase):
    def setUp(self):
        self.app = bootstrap.create_app(TestingConfig)
        self.file_handle , self.app.config['DATABASE'] = tempfile.mkstemp()
        self.app.testing = True
        self.test_client =self.app.test_client()
        with self.app.app_context():
            mainappbp.init_db(self.app)

    def tearDown(self):
        os.close(self.file_handle)
        os.unlink(self.app.config['DATABASE'])

    def test_add_appointments(self):
        with self.app.app_context():
            data = json.dumps({"id":"1","appointment_time":"2017-09-12 08:20:00","description":"this is test data"})
            response = self.test_client.post('/api/v1.0/',data = data,content_type="application/json")
            assert response.content_type == "application/json"
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == "Appointment Saved !"

    def test_appointment_serialize(self):
        appointment = Appointment(1,utils.format_date('2017-09-12 08:20:00'),'this is test data')
        data = json.dumps(appointment.serialize())
        expected = json.dumps({"id":"1","appointment_time":"2017-09-12 08:20:00","description":"this is test data"})
        assert expected == data


    def test_add_appointments_invalid_request(self):
        with self.app.app_context():
            #empty data
            response = self.test_client.post('/api/v1.0/',data = "",content_type="application/json")
            assert response.status_code == 400
            #with content type default
            appointment = Appointment(1,utils.format_date('2017-09-12 08:20:00'),'this is test data')
            data = json.dumps(appointment.serialize())
            response = self.test_client.post('/api/v1.0/',data = data)
            assert response.status_code == 400
            #with Appointment.appointment_time None
            data = json.dumps({"description":"this is test data"})
            response = self.test_client.post('/api/v1.0/',data = data)
            assert response.status_code == 400
            #with Appointment.description None
            data = json.dumps({"appointment_time":"2017-09-12 08:20:00"})
            response = self.test_client.post('/api/v1.0/',data = data)
            assert response.status_code == 400

    def test_get_all_appointments(self):
        with self.app.app_context():
            self.insert_sample(mainappbp.get_db(self.app))
            response = self.test_client.get('/api/v1.0/')
            assert response.status_code== 200
            assert response.content_type =="application/json"
            expected = [
                {
                "id":"1",
                "appointment_time": "2017-09-13 08:08:00",
                "description" : "inserting data #tag"
                },
                {
                "id":"2",
                "appointment_time": "2017-09-13 08:08:30",
                "description" : "another appointment #tag"
                }
            ]

            data = json.loads(response.data)
            for exp, got in zip(expected,data):
                assert exp['id'] == got['id']
                assert exp['appointment_time'] == got['appointment_time']
                assert exp['description'] == got['description']
    def test_get_all_appointments_empty(self):
        with self.app.app_context():
            response = self.test_client.get('/api/v1.0/')
            assert response.status_code== 200
            assert response.content_type =="application/json"
            data = json.loads(response.data)
            assert data['message']== "No appointments made !"


    def test_get_by_description(self):
        with self.app.app_context():
            self.insert_sample(mainappbp.get_db(self.app))
            keyword = "serting"
            response = self.test_client.get('/api/v1.0/'+keyword)
            assert response.status_code == 200
            assert response.content_type == "application/json"
            data = json.loads(response.data)
            assert len(data) == 1
            assert data[0]['id'] == '1'


    def insert_sample(self,db):
        query = """INSERT INTO tbl_appointments (appointment_time, description ) VALUES
            ('2017-09-13 08:08:00','inserting data #tag'),
            ('2017-09-13 08:08:30','another appointment #tag')
            """
        db.cursor().execute(query)
        db.commit()



if __name__=="__main__":
    unittest.main()
