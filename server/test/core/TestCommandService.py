import os
import sys
sys.path.append('../../')
import random
import unittest
import json
from core.Controller.CommandService import *

class TestCommandService(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_ParseCommand(self):
        """test for ParseCommand"""
        print ParseCommand(1, '<Command><AddObject metaobject_id="1" x="100" y="120" diagram_id="1"/></Command>')
    #        self.assertEqual(True, result)
    
    def test_GetDiagram(self):
        """test for GetDiagram"""
        print GetDiagram(1)
    #        self.assertEqual(True, result)

# do unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestCommandService)

unittest.TextTestRunner(verbosity=2).run(suite)
