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


class TestPasses(test.PassToolsTestCase):

	def setUp(self):
		super(TestPasses, self).setUp()
		self.test_new()

	def runTest(self):
		self.test_list()
		self.test_get()
		self.test_update()
		self.test_push_update()
		self.test_delete()	

	def test_get(self):
		# Next, we'll retrieve the full form of that pass
		# You might retrieve a pass, for example, in preparation for updating it.

		self._test_list()
		retrieved_pass = self.service.get_pass(self.pass_list[0].pass_id)
		print "Retrieved Pass #%s" % self.pass_list[0].pass_id
		print retrieved_pass

		# Now let's create a new pass from a template.
		# Start by retrieving a template using the same method used in Ex1_Templates.py
		# The first two steps are a bit contrived, since you would probably know the ID of the template
		# you wanted to use, but for this example we'll get the whole list and use the latest
	

	def _test_list(self):
		# First, we'll use 'list' to retrieve a list of all passes we own (in abbreviated format)
		# Note that, as with templates, the sort order of the list is most-recent-first.
		print "Retrieve list of all existing Passes owned by this user"
		self.pass_list = self.service.list_passes()
		print "Got a list of %d passes for this user!" % len(self.pass_list)
		if len(self.pass_list) > 0:
		    print "Here's the most recent one: (remember that 'pass_fields' will be None for items returned by 'list')"
		    print self.pass_list[0]


	def test_new(self):	
		template_list = self.service.list_templates()
		template_id = template_list[0].template_id

		template = self.service.get_template(template_id)

		# With the template in hand, you could modify any values for fields you defined in that template, so
		# that the modifications would appear in the pass you create
		# As an example, you might change a primary field value
		# Here's one using a default key name:
		#    template.fields_model["primary1"]["value"] = "10% Off!"
		# And in this one, we set 'user_first_name' as a custom key name when we created the template
		#    template.fields_model["user_first_name"]["value"] = "John"

		# Keep in mind:
		#   - If you marked a field as "Required", you'll have to give it a value here, unless you gave it a default
		#   - If you marked a field as 'Don't show if empty', then if you don't give it a value here, it won't show on the pass

		# Now create a new pass from the template.
		# Of course, we haven't changed any fields (since we don't know what's in your template!),
		# so this pass will look like the template, but by changing the fields as described above,
		# you'll be able to generate one form for many customers, or a unique pass for each customer, or anything in between.
		self.pt_pass = pt_pass.Pass(template_id, template.fields_model)

		print "New Pass from template ID %s" % template_id
		print self.pt_pass
		print self.pt_pass.pass_id

		# There are a few ways to deliver passes to customers (and more to come), several of which involve you distributing
		# the pass file itself...so you'll want to download passes you create.
		# Let's do that, using the 'download' method of a pass.
		# IMPORTANT: you'll want to be sure to give your passes the '.pkpass' extension, or they will not be properly recognized
		# when your customer receives them.
		print "Downloading pass %s" % self.pt_pass.pass_id
		self.pt_pass.download("/tmp/New_Pass.pkpass")

		# Alternatively, the service class can download passes specified by ID
		print "Downloading an id-specified Pass from the service..."
		self.service.download_pass("/tmp/New_Pass_2.pkpass", self.pt_pass.pass_id)

	def test_update(self):
		# Next, we'll update an existing pass, using--surprise!--the 'update' method. In this case, we use the fields
		# from the existing pass, modify them, and call update. In typical usage, you might call 'get' above to retrieve a
		# pass to use as input...we'll the pass we just created, so the script output will allow you to compare before/after update.
		# Make a copy of the fields to operate on
		pass_copy = copy.deepcopy(self.pt_pass)


		# Let's a copy of the fields to operate on
		pass_copy = copy.deepcopy(self.pt_pass)

		# Now set the new data. We're going to imagine that our November offer just expired, and we're setting a '15% off'
		# offer to extend 'til the end of the year:
		for f in ["exp_date", "offer"]:
			if f not in pass_copy.pass_fields:
				pass_copy.pass_fields[f] = {}
		pass_copy.pass_fields["exp_date"]["value"] = "12/31/12"
		pass_copy.pass_fields["offer"]["value"] = "15% Off!!!"

		# Call 'update', passing the modifications as input
		updated_pass = self.pt_pass.update(pass_copy)
		# Alternatively use this form:
		#updated_pass = self.service.update_pass(self.pt_pass_id, pass_copy)

		# Now download the updated pass, and distribute to your users!
		self.service.download_pass("/tmp/DecemberOffer.pkpass", updated_pass.pass_id)
		# Alternatively use this form:

		print "Updated Pass..."
		print self.pt_pass
		# The update will be returned; note that the ID is the same, the serial number is the same,
		# and any changes you passed in have been incorporated.
		# If you send the updated pass to a user who has already installed the previous version,
		# they'll see an "Update" button instead of an "Add" button in the iOS UI.

	def test_push_update(self):
		return_data = self.pt_pass.push_update()		

	def test_delete(self):
		# Finally, let's delete the pass:
		deleted_id = self.pt_pass.pass_id
		print "Delete Pass %s" % deleted_id
		self.pt_pass.delete()
		# Alternatively: self.service.delete_pass(deleted_id)

		# And then try to retrieve it:
		print "Attempted to retrieve deleted pass #%s" % deleted_id
		try:
		    retrieved_pass = self.service.get_pass(deleted_id)
		except:
		    info = sys.exc_info()
		    print info[1]




if __name__ == '__main__':
    unittest.main()
    

