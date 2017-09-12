import sys
sys.path.append('../../')
import os
import tempfile


import unittest

import app.bootstrap as bootstrap

class DBTestCase(unittest.TestCase):
    def setUp(self):
        #set up test with temp db file
        self.file_handle , bootstrap.app.config['DATABASE'] = tempfile.mkstemp()
        bootstrap.app.testing = True
        self.test_client =bootstrap.app.test_client()
        with bootstrap.app.app_context():
            bootstrap.init_db()




    def tearDown(self):
        os.close(self.file_handle)
        os.unlink(bootstrap.app.config['DATABASE'])

    def test_one(self):
        assert True == True

if __name__ == '__main__':
    unittest.main()
