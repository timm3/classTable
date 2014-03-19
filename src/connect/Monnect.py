'''
Created on Mar 2, 2014

@author: Michal
'''

from pymongo import MongoClient 
from collections import namedtuple
from pymongo.errors import *
from data.ClassGeneral import ClassGeneral
from collections import namedtuple
from data.Instructor import Instructor
from data.ClassSection import ClassSection


#==========================================================================  
#
#==========================================================================
class ConnectM(object):

    #==========================================================================  
    #
    #==========================================================================
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
        self.db_name = None
        self.collection_name = None
        
        
    #==========================================================================  
    #
    #==========================================================================
    def connect(self):
        
        try:
            self.client = MongoClient(self.host, self.port)
        except ConnectionFailure:
            print("Connection to [" + self.host + "] at port: " + str(self.port) + "failed.")
        
        print("Connected to [" + self.host + "] at port: " + str(self.port) + ".")    
        


    #==========================================================================  
    #
    #==========================================================================
    def disconnect(self):
        
        if self.client != None:
            self.client.close()
            print("Connection to [" + self.host + "] at port: " + str(self.port) + " closed.")
           

    #==========================================================================  
    #
    #==========================================================================
    def set_database_name(self, db_name):
        
        previous_db_name = self.db_name
        self.db_name = db_name
        
        return previous_db_name
        
        
    #==========================================================================  
    #
    #==========================================================================
    def set_collection(self, collection_name):
        
        previous_collection_name = self.collection_name
        self.collection_name = collection_name
        
        return previous_collection_name
        
        
    #==========================================================================  
    #
    #==========================================================================
    def course_exists(self, course):
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]
    
        check_keys = {'year' : course['year'], 'term' : course['term'], 'code' : course['code'], 'course_id' : course['course_id']}
    
        result = collection.find_one(check_keys)
        
        return result
        
        
    #==========================================================================  
    #
    #==========================================================================
    def course_insert(self, course):
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]
        
        result = collection.insert(course)
        
        return result
        
        
    #==========================================================================  
    #
    #==========================================================================
    def section_exists(self, section):
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]   
        
        check_keys = {'year' : section['year'], 'term' : section['term'], 'crn' : section['crn']}
        
        result = collection.find_one(check_keys)
        
        return result
         
         
    #==========================================================================  
    #
    #==========================================================================
    def section_insert(self, section):  
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]
        
        result = collection.insert(section)
        
        return result  
    
             
    #==========================================================================  
    #
    #==========================================================================
    def course_update(self, query, course):
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]
        
        result = collection.update(query, course)
        
        return result
        
         
    #==========================================================================  
    #
    #==========================================================================
    def insert(self, data):  
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]
        
        result = collection.insert(data)
        
        return result  
        
    #==========================================================================  
    #
    #==========================================================================
    def __str__(self):
        
        self_str = "host: " + str(self.host)
        self_str += " port: " + str(self.port)
        self_str += " databse: " + str(self.db)
        self_str += " collection: " + str(self.collection)
        
        return self_str
    
    
    def get_host(self):
        return self.host
    
    def get_port(self):
        return self.port
    
    def get_db_name(self):
        return self.collection_name
    
    def get_collectionn_name(self):
        return self.collection_name
    
    
'''    
print('script start ConnectM:')
host = 'digitalocean-4.perryhuang.com'
port = 27017

client = ConnectM(host, port)
client.connect()

client.set_database_name('courses')
entries = client.set_collection('courses_general')

ClassGenInfo = namedtuple('ClassGenInfo', 'year term code course_id subject title description credit_hours crns')
class_info = ClassGenInfo('2014', 'spring', 'CS', '428', 'Computer Science', 'Software Engineering II', 'Continuation of CS 427. Software development, management, and maintenance. Project and configuration management, collaborative development models, software quality assurance, interoperability domain engineering and software reuse, and software re-engineering.', ['3', '4'], ['31389', '39377', '40652', ])
aClass = ClassGeneral(class_info)
class_dict = aClass.__dict__

if client.course_exists(class_dict) != None:
    print("entry exists")
else:
    print("NO entry")
    result = client.course_insert(class_dict)
    print(str(result))

instructors = []
instr1 = Instructor('D', 'Marinov')
instr2 = Instructor('A', 'Pranav')
instructors.append(instr1)
instructors.append(instr2)

SectionInfo = namedtuple('SectionInfo', 'year term part_of_term c_type section_number crn building_name room_number start_date end_date days_of_week start end instructors')
section_info = SectionInfo('2013', 'spring', '1', 'LCD', 'Q4', '39377', 'Siebel Center for Comp Sci', '1404', None, None, 'TR   ', '02:00 PM', '03:15 PM', instructors)
section = ClassSection(section_info)
section_dict = section.get_dictionary()

if client.section_exists(section_dict) != None:
    print("Section exists.")
else:
    print("Section doesn't exist")
    result = client.section_insert(section_dict)
    print(str(result))

dbs = client.client.database_names()
for db_str in dbs:
    print("Database: " + db_str)
    db = client.client[db_str]
    cls = db.collection_names()
    for cl in cls:
        print("\tcollection: " + cl)

client.disconnect()
print('script end ConnectM.')
'''




