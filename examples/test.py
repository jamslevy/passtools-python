# -*- coding: ISO-8859-1 -*-
##########################################

# Copyright 2012, Tello, Inc.
##########################################


import unittest
import logging
from passtools import service

# API User:
# STEP 1: You must request an API key from Tello
API_KEY = '3384f7e5-e195-4c2f-94ac-5a1c7ae37b33'
API_VERSION = "1.0.0"
SAVED_TEMPLATE_ID = 13743

class PassToolsTestCase(unittest.TestCase):

	def setUp(self, *args, **kwargs):
		self.service = service.Service(API_KEY)