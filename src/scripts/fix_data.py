'''
Created on Apr 9, 2014

@author: Sam
'''

def convert_credit_hours(collection, cursor):
    for json in cursor:
        credit_hours_list = json['credit_hours']
        if credit_hours_list and isinstance(credit_hours_list[0], str):
            new_credit_hours_list = []
            for s in credit_hours_list:
                if isinstance(s, str):
                    new_credit_hours_list.append(int(s))
                else:
                    new_credit_hours_list.append(s)
            
            collection.update(json, {'$set':{'credit_hours':new_credit_hours_list}})
            print('Updated ' + json['code'] + ' ' + json['course_id'])

def delete_extra_courses(collection, cursor):
    for keep in cursor:
        ex_id = keep['_id']
        check = keep.copy()
        del check['_id']
        del check['credit_hours']
        if collection.find(check).count() > 1:
            remove_query = check.copy()
            remove_query['_id'] = {'$ne':ex_id}
            collection.remove(remove_query)
            collection.update(check, keep, upsert=True)

def delete_extra_sections(collection2, cursor2):
    for keep in cursor2:
        ex_id = keep['_id']
        check = keep.copy()
        del check['_id']
        if collection2.find(check).count() > 1:
            print(collection2.find(check).count())
            remove_query = check.copy()
            remove_query['_id'] = {'$ne': ex_id}
            collection2.remove(remove_query)
            collection2.update(check, keep, upsert=True)
            print(collection2.find(check).count())
            print('NEXT')
        cursor2.close()
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
cursor = collection.find({},timeout=False)

delete_extra_courses(collection, cursor)

collection2 = client_courses.client[client_courses.db_name]['courses_section']
cursor2 = collection2.find({}, timeout=False)

delete_extra_sections(collection2, cursor2)

print('done part 1')

client_courses.disconnect()
client_courses.connect()

convert_credit_hours(collection, cursor)
cursor.close()
        
collection.remove({"credit_hours":{"$in": [None, '0']}})
client_courses.disconnect()