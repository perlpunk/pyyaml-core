import yaml
import unittest

from yamlcore import CoreLoader

class TestVariousFeatures(unittest.TestCase):

    def test_duplicate_keys(self):
        input = """
        a: 1
        a: 2
        """
        data = None
        msg = None
        try:
            data = yaml.load(input, Loader=CoreLoader)
        except yaml.YAMLError as e:
            msg = str(e)
        assert(data == None)
        self.assertRegex(msg, r'found duplicate key')

