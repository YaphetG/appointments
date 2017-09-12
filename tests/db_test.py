import sys
sys.path.append('../')
import os
import tempfile


import unittest

from mainapp import run as bootstrap
from mainapp.blueprints import mainappbp
from mainapp.config.config import TestingConfig
from flask import g

class DBTestCase(unittest.TestCase):
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

    def test_root_url(self):
        resp = self.test_client.get('/')
        assert resp.data== 'Hi world'

    def test_db_connection(self):
        assert mainappbp.connect_db(self.app) != None


if __name__ == '__main__':
    unittest.main()
