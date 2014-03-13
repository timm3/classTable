'''
Created on Mar 2, 2014

@author: Michal
'''

from scraper.MyIllinoisXMLRequest import MyIllinoisXMLRequest
from collections import namedtuple
from scraper.XMLReader import XMLReader
from data.Term import Term

URLInfo = namedtuple('URLInfo', 'year term code course_id crn')


#==========================================================================  
#    
#========================================================================== 
class CalendarYear(object):


    def __init__(self, calendar_year_info):
        self.year = calendar_year_info.year
        
    
    #==========================================================================  
    #    
    #    @param 
    #    @return 
    #========================================================================== 
    def get_children(self):
        
        terms = []
        url_info = URLInfo(self.year, None, None, None, None)
        
        term_data = MyIllinoisXMLRequest.get_data(url_info)
        if term_data == None:
            return None
        
        parsed_term_data = XMLReader.extract_terms_data(term_data)
        if parsed_term_data != None:
            for t in parsed_term_data:
                term = Term(t)
                terms.append(term)
        
        return terms
    
    
    #==========================================================================  
    #    
    #    @param 
    #    @return 
    #========================================================================== 
    def __str__(self):
        
        self_str = "year: " + self.year
        
        return self_str
    
    
'''    
print("script start CalendarYear:")

CalendarYearInfo = namedtuple('CalendarYearInfo', 'year')
cl = CalendarYear(CalendarYearInfo('2014'))

children = cl.get_children()

for c in children:
    print(c.__str__())

print("script end CalendarYear.")
'''