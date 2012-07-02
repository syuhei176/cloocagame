import os
import sys
sys.path.append('../../')
import random
import unittest
import json
from core.Controller.MetaModelService import *

class TestMetaModelService(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_GetMetaDiagram(self):
        """test for GetMetaDiagram"""
        print GetMetaDiagram(1)
    #        self.assertEqual(True, result)

# do unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestMetaModelService)

unittest.TextTestRunner(verbosity=2).run(suite)
