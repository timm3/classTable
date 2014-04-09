'''
Created on Feb 12, 2014

@author: Sam Gegg
@updated: Feb 16, 2014 by Sam Gegg
'''
import unittest
import RateMyProfessorWebScraper.WebScraper as WebScraper
from urllib.request import urlopen

PROFESSOR_HTML = urlopen("http://www.ratemyprofessors.com/ShowRatings.jsp?tid=260254").read()
UNRATED_PROFESSOR_HTML = urlopen("http://www.ratemyprofessors.com/AddRating.jsp?tid=1672106").read()

class Test(unittest.TestCase):


    def testHotness(self):
        self.assertEqual(WebScraper.get_hotness(PROFESSOR_HTML), 13)
        
    def testGetScoreData(self):
        self.assertEqual(WebScraper.get_score_card_data(PROFESSOR_HTML), (4.5, 4.6, 4.3, 3.9))
        
    def testGetGrade(self):
        self.assertEqual(WebScraper.get_grade(PROFESSOR_HTML), "N/A")
        
    def testGetName(self):
        self.assertEqual(WebScraper.get_name(PROFESSOR_HTML), "Hadi Esfahani")
        
    def testIsRatedProfessor(self):
        self.assertTrue(WebScraper.is_rated_professor(PROFESSOR_HTML))
        self.assertFalse(WebScraper.is_rated_professor(UNRATED_PROFESSOR_HTML))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
