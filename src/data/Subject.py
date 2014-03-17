'''
Created on Mar 1, 2014

@author: Michal
'''

from scraper.MyIllinoisXMLRequest import MyIllinoisXMLRequest
from collections import namedtuple
from scraper.XMLReader import XMLReader
from data.ClassGeneral import ClassGeneral

URLInfo = namedtuple('URLInfo', 'year term code course_id crn')

#==========================================================================  
#    
#========================================================================== 
class Subject(object):

    def __init__(self, subject_info):
        self.year = subject_info.year
        self.term = subject_info.term
        self.code = subject_info.code
        self.course_ids = subject_info.course_ids
        
    
    #==========================================================================  
    #    
    #    @param 
    #    @return 
    #========================================================================== 
    def get_children(self):
        
        classes = []
        for course_id in self.course_ids:
            url_info = URLInfo(self.year, self.term, self.code, course_id, None)
           
            class_data = MyIllinoisXMLRequest.get_data(url_info)
            if class_data == None:
                continue
            
            parsed_class_data = XMLReader.extract_class_general_data(class_data)
            class_general = ClassGeneral(parsed_class_data)
            classes.append(class_general)
            
        return classes


    #==========================================================================  
    #    
    #    @param 
    #    @return 
    #==========================================================================     
    def __str__(self):
        
        self_str = "year: " + str(self.year)
        self_str += " term: " + str(self.term)
        self_str += " code: " + str(self.code)
        
        self_str += " course ids:" 
        if self.course_ids == None:
            self_str += " " + str(self.course_ids)
        else:
            for c in self.course_ids:
                self_str += " " + str(c)
        
        return self_str    
    
    
'''    
print("start script Subject:")

SubjectInfo = namedtuple('SubjectInfo', 'year term code course_ids')
ids = ['100', '101', '199', '200', '225', '241', '270', '590', '200']
s = SubjectInfo('2013', 'spring', 'PS', ids)

sub = Subject(s)

print(sub.__str__())

children = sub.get_children()

print(len(children))

for c in children:
    print(c.__str__())

print("end script Subject.")
'''







