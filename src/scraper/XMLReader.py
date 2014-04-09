'''
Created on Feb 27, 2014

@author: Michal
'''

import xml.etree.ElementTree as etree
from collections import namedtuple
from data.Instructor import Instructor
from scraper.MyIllinoisXMLRequest import MyIllinoisXMLRequest


#==========================================================================  
#
#==========================================================================  
class XMLReader(object):
    
    #==========================================================================  
    #    
    #   
    #    @param 
    #    @return 
    #==========================================================================  
    @staticmethod
    def extract_terms_data(xml_input):

        terms = []
        TermInfo = namedtuple('TermInfo', 'year term')
        
        root = etree.fromstring(xml_input)
        
        year = root.find('label')
        if year != None:
            year = year.text
            
        terms_tag = root.find('terms')
        if terms_tag != None:
            for t in terms_tag.iter('term'):
                term = XMLReader.parse_term(t.text)
                term = TermInfo(year, term)
                terms.append(term)
    
        return terms
    
    
    #==========================================================================  
    #    
    #   
    #    @param 
    #    @return 
    #==========================================================================  
    @staticmethod
    def extract_subjects_data(xml_input):
        
        SubjectInfo = namedtuple('SubjectInfo', 'year term code course_ids')
        
        root = etree.fromstring(xml_input)
        parents = root.find('parents')
       
        if parents != None:
            year = parents.find('calendarYear')
            if year != None:
                year = year.text
       
        term = root.find('label')
        if term != None:
            term = XMLReader.parse_term(term.text)
       
        subjects_tag = root.find('subjects')
        subjects = []
        if subjects_tag != None:
            for s in subjects_tag.iter('subject'):
                code = s.get('id')
                
                # get course ids
                course_ids = []
                ids_xml_data = XMLReader.request_data(year, term, code, None, None) 
                if ids_xml_data != None:
                    course_ids = XMLReader.extract_class_ids(ids_xml_data)
                
                # build subject object    
                subject_info = SubjectInfo(year, term, code, course_ids)
                subjects.append(subject_info)
                
        return subjects
          
           
    #==========================================================================  
    #    
    #   
    #    @param 
    #    @return 
    #==========================================================================        
    @staticmethod
    def extract_class_ids(xml_input):
        
        class_ids = []
        
        root = etree.fromstring(xml_input)
        
        courses = root.find('courses')
        if courses != None:
            for c in courses.iter('course'):
                c_id = c.get('id')
                class_ids.append(c_id)
            
        return class_ids
    
    
    #==========================================================================  
    #    request_data gets xml formatted string from MyIllinois appropriate
    #    for passed parameters. If a parameter is not availagble pass None.
    #    @param
    #    @return
    #==========================================================================
    @staticmethod
    def request_data(year, term, code, course_id, crn):
        
        URLInfo = namedtuple('URLInfo', 'year term code course_id crn')
        
        url_info = URLInfo(year, term, code, course_id, crn)
        
        xml_data = MyIllinoisXMLRequest.get_data(url_info)
        if xml_data == None:
            return None
        
        return xml_data
        
        
    #==========================================================================  
    #    
    #   
    #    @param 
    #    @return 
    #========================================================================== 
    @staticmethod
    def extract_class_general_data(xml_input):    

        ClassGenInfo = namedtuple('ClassGenInfo', 'year term code course_id subject title description credit_hours crns')
        
        root = etree.fromstring(xml_input)
        parents = root.find('parents')
        
        if parents != None:
            year = parents.find('calendarYear')
            if year != None:
                year = year.text
            term = parents.find('term')
            if term != None:
                term = XMLReader.parse_term(term.text)
            code = parents.find('subject')
            if code != None:
                subject = code.text
                code = code.get('id')    
                
        course_id = XMLReader.parse_course_id(root.get('id'))
            
        title = root.find('label')
        if title != None:
            title = title.text
            
        description = root.find('description')
        if description != None:
            description = description.text
            
        credit_hours = root.find('creditHours')
        if credit_hours != None:
            credit_hours = XMLReader.parse_credit_hours(credit_hours.text)
                
        crns_tag = root.find('sections')
        if crns_tag != None:
            crns = []  # TODO: move crns = [] above the if.. so if the if is false crns is still declared
            for s in crns_tag.iter('section'):
                crns.append(s.get('id'))
                
        if parents != None:
            class_info = ClassGenInfo(year, term, code, course_id, subject, title, description, credit_hours, crns)
        else:
            class_info = ClassGenInfo(None, None, None, course_id, subject, title, description, credit_hours, crns)
            
        return class_info
    
    
    #==========================================================================  
    #    
    #   
    #    @param 
    #    @return 
    #========================================================================== 
    @staticmethod
    def extract_section_data(xml_input):
        
        SectionInfo = namedtuple('SectionInfo', 'year term part_of_term c_type section_number crn building_name room_number start_date end_date days_of_week start end instructors total_slots open_slots')
        
        root = etree.fromstring(xml_input)
        parents = root.find('parents')
        
        if parents != None:
            year = parents.find('calendarYear')
            if year != None:
                year = year.text
            term = parents.find('term')
            if term != None:
                term = XMLReader.parse_term(term.text)
        
        part_of_term = root.find('partOfTerm')
        if part_of_term != None:
            part_of_term = part_of_term.text
            
        section_number = root.find('sectionNumber')
        if section_number != None:
            section_number = section_number.text
         
        crn = root.get('id') 
            
        start_date = root.find('startDate')
        if start_date != None:
            start_date = start_date.text
            
        end_date = root.find('endDate')
        if end_date != None:
            end_date = end_date.text
                
        meetings_data = root.find('meetings')
        if meetings_data != None:
            meetings_data = XMLReader.extract_meetings_tag(meetings_data)
            section_info = SectionInfo(year, term, part_of_term, meetings_data.c_type, section_number, crn, meetings_data.building_name, meetings_data.room_number, start_date, end_date, meetings_data.days_of_week, meetings_data.start, meetings_data.end, meetings_data.instructors, -1, -1)
        else:
            section_info = SectionInfo(year, term, part_of_term, None, section_number, crn, None, None, start_date, end_date, None, None, None, None, -1, -1)  
                
        return section_info


    #==========================================================================  
    #    Extract class meeting information from xml tree element. Some of the 
    #    data in the input may be missing. For missing data None value is 
    #    assigned.
    #    @param etree element with data in xml hierarchy 
    #    @return namedtuple contains extracted data
    #==========================================================================
    @staticmethod
    def extract_meetings_tag(meetings):
        
        MeetingData = namedtuple('MeetingsData', 'c_type building_name room_number days_of_week start end instructors')
        
        meeting = meetings.find('meeting')
        meeting_data = None
               
        if meeting != None:
            c_type = meeting.find('type')
            if c_type != None:
                c_type = c_type.get('code')
            
            building_name = meeting.find('buildingName')
            if building_name != None:
                building_name = building_name.text
                
            room_number = meeting.find('roomNumber')
            if room_number != None:
                room_number = room_number.text
            
            days_of_week = meeting.find('daysOfTheWeek')
            if days_of_week != None:
                days_of_week = days_of_week.text
                
            start = meeting.find('start')
            if start != None:
                start = start.text
            
            end = meeting.find('end')
            if end != None:
                end = end.text
            
            instructors = meeting.find('instructors')      
            if instructors != None:
                instructors = XMLReader.parse_instructors_tag(instructors)
            
            meeting_data = MeetingData(c_type, building_name, room_number, days_of_week, start, end, instructors)
        
        return meeting_data
    
    
    #==========================================================================  
    #    Extract instructor information from etree element. 
    #    @param etree element with data in xml hierarchy 
    #    @return array of objects Instructor
    #==========================================================================
    @staticmethod
    def parse_instructors_tag(instructors):
        
        instructors_parsed = []
        for instr in instructors.iter('instructor'):
            instructor = Instructor(instr.get('firstName'), instr.get('lastName'))
            instructors_parsed.append(instructor)
        
        return instructors_parsed
    
    
    #==========================================================================  
    #    Extract term in lower case from strong formatted as "Term year".
    #    Ex: "Spring 2013"
    #    @param string
    #    @return string
    #==========================================================================  
    @staticmethod   
    def parse_term(term_str):
        
        tokens = term_str.split(' ')
        
        return tokens[0].lower()
    
    #==========================================================================  
    #    Extract integers from given string.
    #    Ex: "3 credits" or "0 TO 4 credits".
    #    @param string
    #    @return array of integers
    #==========================================================================   
    @staticmethod            
    def parse_credit_hours(credits_str):
        
        credit_list = []
        last = None
        for s in credits_str.split(): 
            if last is not None and s.isdigit():
                credit_list.extend(range(last + 1, int(s) + 1))
                last = None
            elif s.isdigit():
                credit_list.append(int(s))
            elif s.lower() == 'to' and credit_list:
                last = credit_list[len(credit_list) - 1]
                
        for x in credit_list:
            if isinstance(x, str):
                print(credit_list)
                break
        return credit_list
   
   
    #==========================================================================  
    #    Extract course id from a string.
    #    Ex: "AAS 100" or "CS 101".
    #    @param string
    #    @return string representation of course id
    #==========================================================================   
    @staticmethod            
    def parse_course_id(course_str):
        
        course_id = []
        for s in course_str.split(): 
            if s.isdigit():
                course_id = str(s)
                break
        
        return course_id
    
    
'''
print("script start XMLReader:")  

from urllib.request import urlopen 

term_data = urlopen('http://courses.illinois.edu/cisapp/explorer/schedule/2014.xml').read()

terms = XMLReader.extract_terms_data(term_data)

for t in terms:
    print("year: " + str(t.year) + " term: " + str(t.term))

print("script end XMLReader.")
'''






