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
        self.file_handle , self.app.config['DATABASE'] = tempfile.mkstemp()
        self.app.testing = True
        self.test_client =self.app.test_client()
        with self.app.app_context():
            mainappbp.init_db(self.app)


    def tearDown(self):
        os.close(self.file_handle)
        os.unlink(self.app.config['DATABASE'])


    def test_db_connection(self):

        assert mainappbp.connect_db(self.app) != None

    def test_get_db_connxn(self):
        with self.app.app_context():
            connection = mainappbp.get_db(self.app)
            assert g.sqlite_db == mainappbp.get_db(self.app)

if __name__ == '__main__':
    unittest.main()
