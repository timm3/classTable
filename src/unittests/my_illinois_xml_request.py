'''
Created on Mar 5, 2014

@author: Michal
'''
import unittest
from scraper.MyIllinoisXMLRequest import MyIllinoisXMLRequest
from collections import namedtuple

URLInfo = namedtuple('URLInfo', 'year term code course_id crn')

class MyIllinoisXMLRequestTest(unittest.TestCase):


    def test_build_url(self):
        
        url_info = URLInfo('2013', 'spring', 'AAS', None, None)
        url = MyIllinoisXMLRequest.build_url(url_info)

        self.assertEqual('http://courses.illinois.edu/cisapp/explorer/schedule/2013/spring/AAS.xml', url)


    def test_request_data(self):
        
        working_url = 'http://courses.illinois.edu/cisapp/explorer/schedule/2012/spring/AAS.xml'
        
        correct_data = open('test_data/spring2012aas.xml').read()
        results = MyIllinoisXMLRequest.get_data(working_url)
        
        self.assertEquals(results, correct_data)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
