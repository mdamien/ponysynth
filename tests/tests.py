#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

TODO: These tests need to be updated to support the Python 2.7 runtime

"""
import os
import unittest

from google.appengine.ext import testbed

from application import app


class DemoTestCase(unittest.TestCase):
    def setUp(self):
        # Flask apps testing. See: http://flask.pocoo.org/docs/testing/
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()
        # Setups app engine test bed. See: http://code.google.com/appengine/docs/python/tools/localunittesting.html#Introducing_the_Python_Testing_Utilities
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def setCurrentUser(self, email, user_id, is_admin=False):
        os.environ['USER_EMAIL'] = email or ''
        os.environ['USER_ID'] = user_id or ''
        os.environ['USER_IS_ADMIN'] = '1' if is_admin else '0'

    def test_home_redirects(self):
        rv = self.app.get('/')
        assert rv.status == '302 FOUND'    

    def test_displays_no_data(self):
        rv = self.app.get('/songs')
        assert 'No songs yet' in rv.data

    def test_404(self):
        rv = self.app.get('/missing')
        assert rv.status == '404 NOT FOUND'
        assert '<h1>Not found</h1>' in rv.data

    
if __name__ == '__main__':
    unittest.main()
