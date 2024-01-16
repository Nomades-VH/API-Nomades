import unittest

from tests.band.controller import TestController as TestBandController
from tests.auth.controller import TestController as TestAuthController

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(unittest.TestCase)
    test_suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestBandController),
        unittest.TestLoader().loadTestsFromTestCase(TestAuthController)
    ])

    unittest.TextTestRunner().run(test_suite)
