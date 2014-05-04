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
# This class provides communication with the MongoDB database 
# that stores course information.
#==========================================================================
class ConnectM(object):

    #==========================================================================  
    # Class constructor.
    #==========================================================================
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
        self.db_name = None
        self.collection_name = None
        
        
    #==========================================================================  
    # This function opens a connection with the database.
    #==========================================================================
    def connect(self):
        
        try:
            self.client = MongoClient(self.host, self.port)
        except ConnectionFailure:
            print("Connection to [" + self.host + "] at port: " + str(self.port) + "failed.")
        
        print("Connected to [" + self.host + "] at port: " + str(self.port) + ".")    
        


    #==========================================================================  
    # This function closses a connection with the database.
    #==========================================================================
    def disconnect(self):
        
        if self.client != None:
            self.client.close()
            print("Connection to [" + self.host + "] at port: " + str(self.port) + " closed.")
           

    #==========================================================================  
    # This function is a mutator for the database name property.
    # @param db_name string database name
    # @return previous database name 
    #==========================================================================
    def set_database_name(self, db_name):
        
        previous_db_name = self.db_name
        self.db_name = db_name
        
        return previous_db_name
        
        
    #==========================================================================  
    # This function is a mutator for the collection name property.
    # @param sollection_name string name of a collection
    # @return string previous collection name
    #==========================================================================
    def set_collection(self, collection_name):
        
        previous_collection_name = self.collection_name
        self.collection_name = collection_name
        
        return previous_collection_name
        
        
    #==========================================================================  
    # This function checks if a course exists in the database.
    # @param course dictionary with course data
    # @return boolean true if the course is in the database, false if not 
    #==========================================================================
    def course_exists(self, course):
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]
    
        check_keys = {'year' : course['year'], 'term' : course['term'], 'code' : course['code'], 'course_id' : course['course_id']}
    
        result = collection.find_one(check_keys)
        
        return result
        
        
    #==========================================================================  
    # This function inserts a course into the database.
    # @param dictionary course data
    # @return boolean result of the insert: true on success, false on failure
    #==========================================================================
    def course_insert(self, course):
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]
        
        result = collection.insert(course)
        
        return result
        
        
    #==========================================================================  
    # This function checks if the given section exists in the database.
    # @param dictionary section data
    # @return boolean result of the check: true if it's in, false if not 
    #==========================================================================
    def section_exists(self, section):
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]   
        
        check_keys = {'year' : section['year'], 'term' : section['term'], 'crn' : section['crn']}
        
        result = collection.find_one(check_keys)
        
        return result
         
         
    #==========================================================================  
    # This function inserts a section into the database.
    # @param dictionary section data
    # @return boolean result of the insert: true on success, false on failure
    #==========================================================================
    def section_insert(self, section):  
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]
        
        result = collection.insert(section)
        
        return result  
    
             
    #==========================================================================  
    # This function updates an entry in the database.
    # @param query
    # @return  
    #==========================================================================
    def update(self, query, data):
        
        db = self.client[self.db_name]   
        collection = db[self.collection_name]
        
        result = collection.update(query, data, multi=True)
        
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
