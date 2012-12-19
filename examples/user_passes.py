# -*- coding: ISO-8859-1 -*-
##########################################

# Copyright 2012, Tello, Inc.
##########################################

import logging
import sys
import unittest

import copy
from passtools import service, pt_pass

import test

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)


class TestUserPasses(test.PassToolsTestCase):

	def setUp(self):
		super(TestUserPasses, self).setUp()

	def test_user_passes(self):
		
		# Our model DB...
		user_db = [{"first_name": "James", "last_name":"Bond"},
		           {"first_name": "Jimi", "last_name":"Hendrix"},
		           {"first_name": "Johnny", "last_name":"Appleseed"}]

		# You'll have selected the template you want to use...you can find the template ID in the Template Builder UI
		selected_template_id = test.SAVED_TEMPLATE_ID

		# Retrieve your template, so you can fill in the fields
		self.template = self.service.get_template(selected_template_id)

		# Now for each user in your DB, grab the user data, populate the template.fields_model, generate a pass and download it:
		for f in ["fname","lname"]:
			if f not in self.template.fields_model:
				self.template.fields_model[f] = {}
		for user_record in user_db:
		    self.template.fields_model["fname"]["value"] = user_record["first_name"]
		    self.template.fields_model["lname"]["value"] = user_record["last_name"]
		    new_pass = pt_pass.Pass(selected_template_id, self.template.fields_model)
		    new_pass.download("/tmp/%s_%s.pkpass" % (user_record["first_name"], user_record["last_name"]))

		# Now distribute the passes to your users!



if __name__ == '__main__':
    unittest.main()
    




