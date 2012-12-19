# -*- coding: ISO-8859-1 -*-
##########################################

# Copyright 2012, Tello, Inc.
##########################################


from examples import templates, passes, user_passes

import unittest

def run_tests():
	
	for test_case in [passes.TestPasses, templates.TestTemplates, user_passes.TestUserPasses]:
		suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
		unittest.TextTestRunner(verbosity=2).run(suite)



if __name__ == '__main__':
    run_tests()
    