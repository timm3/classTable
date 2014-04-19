'''
Created on Apr 9, 2014

@author: Sam
'''

from connect.Monnect import ConnectM
from scraper.XMLReader import XMLReader
#from pymongo.errors import PyMongoError
#from pprint import pprint

def add_time_nums(collection):
    #bulk = collection.initialize_unordered_bulk_op()
    for start in collection.distinct('start'):
        if start != 'ARRANGED' and start is not None:
            collection.update({'start': start}, {'$set': {'start_num': XMLReader.parse_time(start)}})
    for end in collection.distinct('end'):
        if end != 'ARRANGED' and end is not None:
            collection.update({'end': end}, {'$set': {'end_num': XMLReader.parse_time(end)}})
    #try:
        #bulk.execute()
    #except PyMongoError as bwe:
        #pprint(bwe.details)
    

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
            
def delete_extra_profs(collection, cursor):
    for keep in cursor:
        ex_id = keep['_id']
        check = keep.copy()
        del check['_id']
        if collection.find(check).count() > 1:
            remove_query = check.copy()
            remove_query['_id'] = {'$ne':ex_id}
            collection.remove(remove_query)
            collection.update(check, keep, upsert=True)

def delete_extra_sections(collection2, cursor2):
    for keep in cursor2:
        ex_id = keep['_id']
        check = keep.copy()
        crn_check = {'crn':check['crn']}
        find_crn = collection2.find(crn_check)
        for other in find_crn:
            check.update(other)
        del check['_id']
        print(find_crn.count())
        if collection2.find(crn_check).count() > 1:
            print('Deleting')
            remove_query = crn_check.copy()
            remove_query['_id'] = {'$ne': ex_id}
            collection2.remove(remove_query)
            print(collection2.find(crn_check).count())
            collection2.update(crn_check, check, upsert=True)
            print(collection2.find(crn_check).count())
            print('Done deleting')
    cursor2.close()

'''
Script gets all subjects in a given term of a given year.
'''
HOST = 'digitalocean-4.perryhuang.com'
PORT = 27017

client_courses = ConnectM(HOST, PORT)
client_courses.connect()
client_courses.set_database_name('courses')
#client_courses.set_collection('courses_general')

#collection = client_courses.client[client_courses.db_name][client_courses.collection_name]
#cursor = collection.find({},timeout=False)

#delete_extra_courses(collection, cursor)

#collection2 = client_courses.client[client_courses.db_name]['courses_section']
#cursor2 = collection2.find({}, timeout=False)

#print(cursor2.count())
#add_time_nums(collection2)

#print('done part 1')

prof_collection = client_courses.client['professors']['professors']
prof_cursor = prof_collection.find({}, timeout=False)
delete_extra_profs(prof_collection, prof_cursor)

client_courses.disconnect()
#client_courses.connect()

#convert_credit_hours(collection, cursor)
#cursor.close()
        
#collection.remove({"credit_hours":{"$in": [None, '0']}})
#client_courses.disconnect()