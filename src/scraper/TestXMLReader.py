'''
Created on Apr 8, 2014

@author: Sam
'''
import unittest
from XMLReader import XMLReader


class Test(unittest.TestCase):


    def testParseCreditHours(self):
        string = "3 or 4 credits"
        self.xmlreader = XMLReader()
        self.assertEqual(self.xmlreader.parse_credit_hours(string), [3, 4])

    def testParseCreditHoursRange(self):
        string = "0 TO 4 credits"
        self.xmlreader = XMLReader()
        self.assertEqual(self.xmlreader.parse_credit_hours(string), [0, 1, 2, 3, 4])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testParseCreditHours']
    unittest.main()
