'''
Created on Feb 12, 2014

@author: Sam Gegg
@updated: Feb 16, 2014 by Sam Gegg
'''
import unittest
import KoofersWebScraper
from urllib.request import urlopen

CLASS_HTML = urlopen("https://www.koofers.com/university-of-illinois-urbana-champaign-uiuc/atms/120-severe-and-hazardous-weather/").read()

class Test(unittest.TestCase):


    def testGPA(self):
        self.assertEqual(KoofersWebScraper.get_gpa(CLASS_HTML), 3.78)
        
    def testProfRating(self):
        self.assertEqual(KoofersWebScraper.get_prof_rating(CLASS_HTML), 4.94)
        
    def testCourseGradeBreakdown(self):
        self.assertEqual(KoofersWebScraper.get_course_grade_breakdown(CLASS_HTML), [84.12, 12.32, 2.64, 0.78, 0.14])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()