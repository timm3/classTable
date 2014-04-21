
'''
Created on Mar 5, 2014

@author: Michal
'''

from collections import namedtuple
from data.Term import Term
from connect.Monnect import ConnectM

from KoofersWebScraper.KoofersWebScraper import get_course_list
from RateMyProfessorWebScraper.WebScraper import get_prof_list

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

subjects = get_subjects('2014', 'spring')



'''
#SUBJECT (like Computer Science, Asian American Studies, etc.)
SubjectInfo = namedtuple('SubjectInfo', 'year term code course_ids')
subject_info = SubjectInfo('2014', 'spring', 'AAS', {'100', '120', '246', '265', '281', '283', '286', '299', '310', '317', '328', '365', '397', '435', '479', '539', '561'})
subject = Subject(subject_info)
subjects = {subject}
'''

for s in subjects:
    print('Subject: ' + s.code)
    # for each subject get all classes
    subject_classes = s.get_children()
    
    # add subject's classes to database
    for sc in subject_classes:
        print('\tClass: ' + sc.title)
        class_dict = sc.__dict__
        
        # add class to database
        if client_courses.course_exists(class_dict) is None:
            client_courses.course_insert(class_dict)

        # add classe's sections to database
        class_sections = None
        while not class_sections:
            try:
                class_sections = sc.get_children()
            except TimeoutError:
                print("TimeoutError")
                
        for cs in class_sections:
            print('\t\tSection: ' + cs.crn)
            class_section_dict = cs.get_dictionary()
        
            if client_sections.section_exists(class_section_dict) is None:
                client_sections.section_insert(class_section_dict)
                
print("Subjects: ")
client_subject_col = client_courses.client[client_courses.db_name][client_courses.collection_name]
# client_courses.client[client_courses.db_name].drop_collection(client_courses.collection_name)        #remove all courses
print(client_subject_col.find({'year' : '2014'}).count())

print("Sections: ")
client_section_col = client_sections.client[client_sections.db_name][client_sections.collection_name]
# client_sections.client[client_sections.db_name].drop_collection(client_sections.collection_name)    #remove all sections
print(client_section_col.find({'year' : '2014'}).count())

client_sections.disconnect()
client_courses.disconnect()
client_courses.connect()

client_profs = ConnectM(HOST, PORT)
client_profs.connect()
client_profs.set_database_name('professors')
client_profs.set_collection('professors')

print('Adding Koofers course data')

course_list = get_course_list()
for course in course_list:
    print(course)
    print(course.dataToUpdateDoc())
    client_courses.update({"course_id": course.course_number, "code": course.subject_code}, course.dataToUpdateDoc())
    
print('Adding RateMyProfessors professor data')
    
prof_list = get_prof_list()
for prof in prof_list:
    print(prof)
    data_doc = prof.dataToDoc()
    update_check = {'first_name': data_doc['first_name'], 'last_name': data_doc['last_name']}
    client_profs.update(update_check, data_doc)

client_profs.disconnect()
client_courses.disconnect()
