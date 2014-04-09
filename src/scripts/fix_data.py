'''
Created on Apr 9, 2014

@author: Sam
'''

from connect.Monnect import ConnectM

'''
Script gets all subjects in a given term of a given year.
'''
HOST = 'digitalocean-4.perryhuang.com'
PORT = 27017

client_courses = ConnectM(HOST, PORT)
client_courses.connect()
client_courses.set_database_name('courses')
client_courses.set_collection('courses_general')

collection = client_courses.client[client_courses.db_name][client_courses.collection_name]
cursor = collection.find({})

for json in cursor:
    credit_hours_list = json['credit_hours']
    if credit_hours_list and isinstance(credit_hours_list[0], str):
        new_credit_hours_list = []
        for s in credit_hours_list:
            if isinstance(s, str):
                new_credit_hours_list.append(int(s))
            else:
                new_credit_hours_list.append(s)
        collection.update(json, {'$set':{'credit_hours': new_credit_hours_list}})
        print('Updated ' + json['code'] + ' ' + json['course_id'])
client_courses.disconnect()
