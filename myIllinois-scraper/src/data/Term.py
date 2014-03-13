'''
Created on Mar 2, 2014

@author: Michal
'''

from scraper.MyIllinoisXMLRequest import MyIllinoisXMLRequest
from scraper.XMLReader import XMLReader
from collections import namedtuple
from data.Subject import Subject

URLInfo = namedtuple('URLInfo', 'year term code course_id crn')

#==========================================================================  
#    
#==========================================================================
class Term(object):

    def __init__(self, term_info):
        self.year = term_info.year
        self.term = term_info.term
        
        
    #==========================================================================  
    #    This function takes really f*g long time before it returns.
    #    Could use several separate processes/threads to run it.
    #   
    #    @param 
    #    @return 
    #==========================================================================
    def get_children(self):

        subjects = []
        
        url_info = URLInfo(self.year, self.term, None, None, None)
        subject_data = MyIllinoisXMLRequest.get_data(url_info)
        
        if subject_data == None:
            return None
        
        parsed_subject_data = XMLReader.extract_subjects_data(subject_data)
        
        for s in parsed_subject_data:
            subject = Subject(s)
            subjects.append(subject)
            
        return subjects
        
        
    #==========================================================================  
    #    
    #   
    #    @param 
    #    @return 
    #==========================================================================    
    def __str__(self):
        
        self_str = "year: " + str(self.year)
        self_str += " term: " + str(self.term)
        
        return self_str
    
'''    
print("script start Term:")

TermInfo = namedtuple('TermInfo', 'year term')
term_info = TermInfo('2013', 'spring')

term = Term(term_info)

print(term.__str__())

children = term.get_children()
for c in children:
    print(c.__str__())

print("script end Term:")
'''
   
   
   
   
   
   
   