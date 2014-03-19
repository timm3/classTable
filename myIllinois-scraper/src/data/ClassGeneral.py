'''
Created on Feb 28, 2014

@author: Michal
'''

from collections import namedtuple
from scraper.MyIllinoisXMLRequest import MyIllinoisXMLRequest
from scraper.XMLReader import XMLReader
from data.ClassSection import ClassSection
from pymongo import MongoClient 

#==========================================================================  
#
#==========================================================================
class ClassGeneral(object):

    def __init__(self, class_info):
        self.year = class_info.year
        self.term = class_info.term
        self.code = class_info.code
        self.course_id = class_info.course_id
        self.subject = class_info.subject
        self.title = class_info.title
        self.description = class_info.description
        self.credit_hours = class_info.credit_hours
        self.crns = class_info.crns
    
    
    #==========================================================================  
    #
    #==========================================================================
    def get_children(self):
        
        URLInfo = namedtuple('URLInfo', 'year term code course_id crn')
        sections = []
        
        for crn in self.crns:
            url_info = URLInfo(self.year, self.term, self.code, self.course_id, crn)
            
            section_data = MyIllinoisXMLRequest.get_data(url_info)
            if section_data == None:
                continue
            
            parsed_section_data = XMLReader.extract_section_data(section_data)
            class_section = ClassSection(parsed_section_data)
            
            sections.append(class_section)
            
        return sections
    
    
    #==========================================================================  
    #
    #==========================================================================
    def __str__(self):
        
        self_str = "year: " + str(self.year)
        self_str += " term: " + str(self.term)
        self_str += " code: " + str(self.code)
        self_str += " course_id: " + str(self.course_id)
        self_str += " subject: " + str(self.subject)
        self_str += " title: " + str(self.title)
        self_str += " description: " + str(self.description)
        self_str += " credit_hours:"
        
        if self.credit_hours == None:
            self_str += " " + str(self.credit_hours)
        else:
            for c in self.credit_hours:
                self_str += " " + c
        
        self_str += " sections:"
        
        if self.crns == None:
            self_str += " " + str(self.crns)
        else:
            for s in self.crns:
                self_str += " " + str(s)
                
        return self_str
    
    
'''
print("script start ClassGeneral:")
SectionInfo = namedtuple('SectionInfo', 'year term part_of_term type section_number crn building_name room_number start_date end_date days_of_week start end instructors')
ClassGenInfo = namedtuple('ClassGenInfo', 'year term code course_id subject title description credit_hours crns')

year = "2013" 
term = "spring"
code = "PS"
course_id = "590"
subject = "Political Science"
title = "Research in Selected Topics"
description = "Research in selected topics by arrangement with the instructor."
credit_hours = ['2', '12']
crns = ['10195', '26057', '26048', '26365', '57689']

class_info = ClassGenInfo(year, term, code, course_id, subject, title, description, credit_hours, crns)

cls = ClassGeneral(class_info)

#create sections objects
children = cls.get_children()

for child in children:
    print(child.__str__())
    
print("script end ClassGeneral.")   
'''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    