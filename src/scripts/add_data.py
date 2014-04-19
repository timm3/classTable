
'''
Created on Mar 17, 2014

@author: Sam Gegg
'''
from connect.Monnect import ConnectM

from KoofersWebScraper.KoofersWebScraper import get_course_list
from RateMyProfessorWebScraper.WebScraper import get_prof_list

'''
Script gets all subjects in a given term of a given year.
'''
HOST = 'digitalocean-4.perryhuang.com'
PORT = 27017

client_courses = ConnectM(HOST, PORT)
client_courses.connect()
client_courses.set_database_name('courses')
client_courses.set_collection('courses_general')

client_profs = ConnectM(HOST, PORT)
client_profs.connect()
client_profs.set_database_name('professors')
client_profs.set_collection('professors')

print('Adding Koofers course data')

course_list = get_course_list()
for course in course_list:
    print(course)
    client_courses.course_update({"course_id": course.course_number, "code": course.subject_code}, course.dataToUpdateDoc())
  
client_courses.disconnect()

print('Finished adding course data')
    
print('Adding RateMyProfessors professor data')
    
prof_list = get_prof_list()
for prof in prof_list:
    print(prof)
    data_doc = prof.dataToDoc()
    update_check = {'first_name': data_doc['first_name'], 'last_name': data_doc['last_name']}
    client_profs.update(update_check, data_doc)

client_profs.disconnect()

print('Finished adding professor data')
