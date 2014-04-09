'''
Created on Feb 28, 2014

@author: Michal
'''

class Instructor(object):

    def __init__(self, first_name, last_name):
        
        self.first_name = first_name
        self.last_name = last_name
        
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def __str__(self):
        
        self_str = "first name: " + self.get_first_name() + " last name: " + self.get_last_name()
        
        return self_str
