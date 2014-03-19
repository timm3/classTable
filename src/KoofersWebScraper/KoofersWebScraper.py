'''
Created on Feb 19, 2014

@author: Sam Gegg
@updated: Mar 2, 2014 by Sam Gegg
'''

from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import urlopen
import re
import queue
from KoofersWebScraper.KoofersCourseData import KoofersCourseData as CourseData

BASE_SCHOOL_URL = "https://www.koofers.com/university-of-illinois-urbana-champaign-uiuc/browse?s=4&p=1"
BASE_PAGE_URL = "https://www.koofers.com"
TEST_COURSE_URL = "https://koofers.com/university-of-illinois-urbana-champaign-uiuc/atms/120-severe-and-hazardous-weather/"

'''
SCANF %f simulator taken from
http://docs.python.org/3.1/library/re.html#simulating-scanf
'''
SCAN_FOR_FLOAT = "[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?"

'''
Enum for indexes of section of HTML
'''
class Indexes:
    GPA, Prof_Rating, Prof_Num, Past_Tests_and_Quizzes, Teacher_Ratings = range(5)

'''
Puts all the links to courses' pages on the queue
Helper function for construct_URL_queue
'''
def get_course_links(html, url_queue):
    course_strainer = SoupStrainer(class_="title")
    course_soup = BeautifulSoup(html, parse_only = course_strainer)
    for link in course_soup.find_all('a') :
        url_queue.put(BASE_PAGE_URL + link['href'])
 
'''
Returns a queue of URLs for courses' pages which can be found from the BASE_SCHOOL_URL
'''   
def construct_course_URL_queue():
    url_queue = queue.Queue()
    course_links_html = urlopen(BASE_SCHOOL_URL).read()
    next_course_links_html_strainer = SoupStrainer(class_="page_links")
    while True:
        get_course_links(course_links_html, url_queue)
        next_course_links_html = BeautifulSoup(course_links_html, parse_only=next_course_links_html_strainer).find(class_="next")
        if next_course_links_html:
            course_links_html = urlopen(BASE_PAGE_URL + "/university-of-illinois-urbana-champaign-uiuc/" + next_course_links_html['href']).read()
        else: break
    return url_queue

'''
Helper function to extract data from the HTML page's main data source, that which uses Indexes 
'''
def get_data(html, index):
    strainer = SoupStrainer(style="margin-bottom:10px;")
    right_box_soup = BeautifulSoup(html, parse_only = strainer)
    div = right_box_soup.find_all('div', recursive=False)[index]
    return div.find('a').string
    
'''
Returns the average grade as GPA of  a student of this course as float data
'''
def get_gpa(html):
    gpa = get_data(html, Indexes.GPA)
    try:
        return float(gpa)
    except ValueError:
        return None

  
'''
Returns the average professor's rating for this course as float data from 0 to 5 stars
'''  
def get_prof_rating(html):
    return float(re.findall(SCAN_FOR_FLOAT, get_data(html, Indexes.Prof_Rating))[0][0])

'''
Returns the course grade breakdown of this class a list of floats as follows
%A, %B, %C, %D, %F
'''
def get_course_grade_breakdown(html):
    javascript_strainer = SoupStrainer(type='text/javascript')
    javascript = BeautifulSoup(html, parse_only = javascript_strainer)
    for spoon in javascript:
        if spoon.string:
            variable_namings = re.findall("(?<={y: ).*?(?=,)", spoon.string)
            if len(variable_namings):
                percentages = []
                for string in variable_namings:
                    percentages.append(float(string))
                return percentages

def get_course_id(html):
    course_id_strainer = SoupStrainer(class_="course_number")
    course_id_html = BeautifulSoup(html, parse_only = course_id_strainer)
    return course_id_html.find(class_="course_number").string
    

'''
Returns a list of tuples containing the following information about a course:
    GPA(float), ProfRating(float), 
    [%A(float), %B(float), %C(float), %D(float), %F(float)]
'''
def get_course_list():
    url_queue = construct_course_URL_queue()
    course_list = []
    while not url_queue.empty():
        course_url = url_queue.get()
        course_html = urlopen(course_url).read()
        
        gpa = get_gpa(course_html)
        if not gpa: continue
        prof_rating = get_prof_rating(course_html)
        grade_breakdown = get_course_grade_breakdown(course_html)
        course_id = get_course_id(course_html)
        if grade_breakdown is None: continue
        course_data = CourseData(gpa, prof_rating, grade_breakdown, course_id, course_url)
        course_list.append(course_data)
        
    return course_list


if __name__ == '__main__':
    course_list = get_course_list()
        
    for course_data in course_list:
        print(course_data + "\n")