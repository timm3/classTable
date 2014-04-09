'''
Created on Mar 1, 2014

@author: Michal
'''

from urllib.request import urlopen
from urllib.error import HTTPError
from collections import namedtuple

BASE_MYILLINOIS_URL = "http://courses.illinois.edu/cisapp/explorer/schedule"

URLInfo = namedtuple('URLInfo', 'year term code course_id crn')

#==========================================================================  
#    Request course's data from CIS - Data Explorer App.
#    http://courses.illinois.edu/cisdocs/explorer
#==========================================================================
class MyIllinoisXMLRequest(object):

    #==========================================================================  
    #    TODO: define behavior in case of request exceptions such as error 404,
    #    500, ...
    
    #    Get 
    #========================================================================== 
    @staticmethod
    def get_data(url_info):
        
        try:
            url = MyIllinoisXMLRequest.build_url(url_info)
            raw_xml_data = MyIllinoisXMLRequest.request_data(url)
            return raw_xml_data
        
        except HTTPError:
            return None
        
    
    #==========================================================================  
    #
    #========================================================================== 
    @staticmethod
    def build_url(url_info):
        
        url = BASE_MYILLINOIS_URL
        
        for part in url_info:
            if part != None:
                url += '/' + part
            else:
                break
            
        url += '.xml'
        
        return url
    
    
    #==========================================================================  
    #
    #========================================================================== 
    @staticmethod
    def request_data(request_url):
        
        raw_data = urlopen(request_url).read()
        decoded_raw_data = raw_data.decode('utf-8')
       
        return decoded_raw_data
    
