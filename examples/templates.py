# -*- coding: ISO-8859-1 -*-
##########################################

# Copyright 2012, Tello, Inc.
##########################################

import logging
import sys
import unittest

from passtools import service, template
import test

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.CRITICAL)



class TestTemplates(test.PassToolsTestCase):

	def setUp(self):
		super(TestTemplates, self).setUp()
		self.existing_template_owned_by_other = 220
		self.template_id = test.SAVED_TEMPLATE_ID

	def test_list(self):
		"""
		The 'list' operation retrieves a list of all your templates.
		The retrieved items do not include the complete template.fields_model,
		but instead are intended to provide quick lookup info.
		Note the sort order of the list is most-recent-first.
		"""
		print "Retrieve list of all existing Templates owned by this user"
		template_list = self.service.list_templates()
		print "Got a list containing %d templates for this user!" % len(template_list)
		if len(template_list) > 0:
		    print "The most recently-created is this:"
		    print template_list[0]
		    return template_list[0]


	def test_get(self):	

		"""
		Now we'll use 'get_template' to retrieve the complete form of that latest template.
		You might retrieve a template, for example, in preparation for creating an pass.
		
		"""
		print "Retrieve existing Template #%d" % self.template_id
		retrieved_template = self.service.get_template(self.template_id)
		print retrieved_template
		print ""

		#Or we can instantiate the template using its ID.
		print "Instantiate Template #%d" % self.template_id
		template_instance = template.Template(self.template_id)
		print template_instance
		print ""

	def _test_delete(self):
		"""
		Let's delete that template
		"""
		print "Delete Template #%d" % self.template_id
		template_instance = template.Template(self.template_id)
		template_instance.delete()
		# Alternatively: service.delete_template(self.template_id)

		# And then try to retrieve it:
		print "Attempted to retrieve deleted template #%s" % self.template_id
		try:
		    retrieved_template = self.service.get_template(self.template_id)
		except:
		    info = sys.exc_info()
		    print info[1]

	def test_errors(self):
		"""
		Finally, let's try to retrieve a template owned by someone else.
		This template doesn't belong to me, so I should see errors.
		"""
		print "Attempt to retrieve someone else's template"
		try:
		    retrieved_template = self.service.get_template(self.existing_template_owned_by_other)
		except:
		    info = sys.exc_info()
		    print info[1]



if __name__ == '__main__':
    unittest.main()
    
