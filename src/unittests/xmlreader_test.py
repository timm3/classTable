'''
Created on Mar 5, 2014

@author: Michal
'''
import unittest
from scraper.XMLReader import XMLReader

class XmlReaderTest(unittest.TestCase):

    #==========================================================================  
    #    
    #========================================================================== 
    def test_extract_terms_data(self):
        
        file = open('test_data/2014.xml')
        
        extract_result = XMLReader.extract_terms_data(file.read())
        
        self.assertEqual(3, len(extract_result))
        
        
    #==========================================================================  
    #    
    #==========================================================================    
    def test_extract_subjects_data(self):
        
        file = open('test_data/spring2013.xml')
        
        extract_result = XMLReader.extract_subjects_data(file.read())
        
        self.assertEqual(187, len(extract_result))


    #==========================================================================  
    #    
    #========================================================================== 
    def test_extract_class_ids(self):
        
        file = open('test_data/spring2013aas.xml')
        
        extract_result = XMLReader.extract_class_ids(file.read())

        self.assertEqual(16, len(extract_result))
         
    #==========================================================================  
    #    
    #========================================================================== 
    def test_extract_class_general_data(self):
        
        file = open('test_data/spring2012aas100.xml')
        
        extract_result = XMLReader.extract_class_general_data(file.read())
        
        self.assertEqual('2012', extract_result.year)
        self.assertEqual('spring', extract_result.term)
        self.assertEqual('AAS', extract_result.code)
        self.assertEqual('100', extract_result.course_id)
        self.assertEqual('Asian American Studies', extract_result.subject)
        self.assertEqual('Intro Asian American Studies', extract_result.title)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()