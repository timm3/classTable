'''
Created on Feb 28, 2014

@author: Michal
'''


#==========================================================================  
#
#==========================================================================
class ClassSection(object):

    def __init__(self, section_info):
        self.year = section_info.year
        self.term = section_info.term
        self.part_of_term = section_info.part_of_term
        self.c_type = section_info.c_type
        self.section_number = section_info.section_number
        self.crn = section_info.crn
        self.building_name = section_info.building_name
        self.room_number = section_info.room_number
        self.start_date = section_info.start_date
        self.end_date = section_info.end_date
        self.days_of_week = section_info.days_of_week
        self.start = section_info.start
        self.end = section_info.end
        self.instructors = section_info.instructors
        self.total_slots = section_info.total_slots
        self.open_slots = section_info.open_slots
        
    #==========================================================================  
    #
    #==========================================================================
    def __str__(self):
        
        self_str = "year: " + str(self.year)
        self_str += " term: " + str(self.term)
        self_str += " part of term: " + str(self.part_of_term)
        self_str += " c_type: " + str(self.c_type)
        self_str += " section number: " + str(self.section_number)
        self_str += " crn: " + str(self.crn)
        self_str += " building name: " + str(self.building_name)
        self_str += " room number: " + str(self.room_number)
        self_str += " start date: " + str(self.start_date)
        self_str += " end date: " + str(self.end_date)
        self_str += " days of week: " + str(self.days_of_week)
        self_str += " start: " + str(self.start)
        self_str += " end: " + str(self.end)
        self_str += " instructors:"
       
        if self.instructors == None:
            self_str += str(self.instructors)
        else:
            for i in self.instructors:
                self_str += " " + i.get_first_name() + " " + i.get_last_name()
       
        self_str += " total_sots: " + str(self.total_slots)
        self_str += " open_slots: " + str(self.open_slots)
        
        return self_str         
            
    #==========================================================================  
    #    Change array of references to Instructor objects to array of __dict__
    #    of each of the objects so that this objects __dict__ holds values.
    #    @return dictionary
    #==========================================================================        
    def get_dictionary(self):
        
        section_dict = self.__dict__
        instructor_objects = section_dict.pop('instructors')
        
        instructors = []
        for e in instructor_objects:
            instructors.append(e.__dict__)
            
        section_dict['instructors'] = instructors
        
        return section_dict


'''
print("script start ClassSection:")

from collections import namedtuple
from data.Instructor import Instructor

SectionInfo = namedtuple('SectionInfo', 'year term part_of_term c_type section_number crn building_name room_number start_date end_date days_of_week start end instructors total_slots open_slots')

year = "2014" 
term = "spring"
part_of_term = "1"
c_type = "LEC"
section_number = "LA1"
crn = "45987"
building_name = "Siebel Center"
room_number = "1404"
start_date = "2013-01-14-06:00"
end_date = "2013-05-01-05:00"
days_of_week = "MWF"
start = "12:00 PM"
end = "12:50 PM"
instructors = [Instructor("E", "Guntner"), Instructor("A", "Harek")]
total_slots = -1
open_slots = -1

section_info = SectionInfo(year, term, part_of_term, c_type, section_number, crn, building_name, room_number, start_date, end_date, days_of_week, start, end, instructors, total_slots, open_slots)

sect = ClassSection(section_info)
print(sect)

print("script end ClassSection.")         
'''             
                 
                 
                 