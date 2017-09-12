import sys
sys.path.append('../../')
import os
import tempfile


import unittest

from mainapp import bootstrap
from mainapp.config.config import TestingConfig
class DBTestCase(unittest.TestCase):
    def setUp(self):
        #set up test with temp db file
        bootstrap.app.config.from_object(TestingConfig)
        self.file_handle , bootstrap.app.config['DATABASE'] = tempfile.mkstemp()
        bootstrap.app.testing = True
        self.test_client =bootstrap.app.test_client()
        with bootstrap.app.app_context():
            bootstrap.init_db()



    def tearDown(self):
        pass
        #os.close(self.file_handle)
        #os.unlink(bootstrap.app.config['DATABASE'])

    def test_one(self):
        resp = self.test_client.get('/')        
        assert resp.data== 'Hi world'

if __name__ == '__main__':
    unittest.main()
