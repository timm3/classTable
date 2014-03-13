'''
Created on Mar 5, 2014

@author: Michal
'''

from collections import namedtuple
from data.ClassGeneral import ClassGeneral
from collections import namedtuple
from data.ClassSection import ClassSection
from data.Term import Term
from data.Subject import Subject
from connect.Monnect import ConnectM

def get_subjects(year, term):
    
    TermInfo = namedtuple('TermInfo', 'year term')
    term_info = TermInfo(year, term)
    
    term = Term(term_info)
    subjects = term.get_children()
    
    return subjects


def get_courses_general(subject):
    
    subject_classes = subject.get_children()
    
    return subject_classes



'''
Script gets all subjects in a given term of a given year.
'''
HOST = 'digitalocean-4.perryhuang.com'
PORT = 27017

client_courses = ConnectM(HOST, PORT)
client_courses.connect()
client_courses.set_database_name('courses')
client_courses.set_collection('courses_general')

client_sections = ConnectM(HOST, PORT)
client_sections.connect()
client_sections.set_database_name('courses')
client_sections.set_collection('courses_section')

sections_collection = client_sections.client[client_sections.db_name][client_sections.collection_name]


for e in sections_collection.find():
    print(e)

print(sections_collection.find({'year' : '2014'}).count())

#subjects = get_subjects('2014', 'spring')
#SUBJECT (like Computer Science, Asian American Studies, etc.)
SubjectInfo = namedtuple('SubjectInfo', 'year term code course_ids')
subject_info = SubjectInfo('2014', 'spring', 'AAS', {'100', '120', '246', '265', '281', '283', '286', '299', '310', '317', '328', '365', '397', '435', '479', '539', '561'})
subject = Subject(subject_info)
subjects = {subject}


for s in subjects:
    print('Subject: ' + s.code)
    #for each subject get all classes
    subject_classes = s.get_children()
    
    #add subject's classes to database
    for sc in subject_classes:
        print('\tClass: ' + sc.title)
        class_dict = sc.__dict__
        
        #add class to database
        if None == client_courses.course_exists(class_dict):
            client_courses.course_insert(class_dict)

        #add classe's sections to database
        class_sections = sc.get_children()
        for cs in class_sections:
            print('\t\tSection: ' + cs.crn)
            class_section_dict = cs.get_dictionary()
        
            if None == client_sections.section_exists(class_section_dict):
                client_sections.section_insert(class_section_dict)

client_courses.disconnect()
client_sections.disconnect()


print(sections_collection.find({'year' : '2014'}).count())