'''
Created on Jan 27, 2014

@author: Sam Gegg
@updated: Mar 2, 2014 by Sam Gegg
'''

from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import urlopen
import re
import queue
from RateMyProfessorWebScraper.ProfessorData import RateMyProfessorData as ProfessorData

BASE_SCHOOL_URL = "http://www.ratemyprofessors.com/SelectTeacher.jsp?sid=1112&pageNo=1"


'''
Puts all the links to professors' pages which may have been rated on the queue
Helper function for construct_URL_queue
'''

def get_professor_links(prof_soup, url_queue):
    for prof in prof_soup:
        #=======================================================================
        # Checks if link goes to professor with ratings:
        # Links for professors without ratings show up as AddRatings... not ShowRatings...
        # This method is imperfect: ShowRatings link may redirect to AddRatings link
        # For this reason we later check again with is_rated_professor
        #=======================================================================
        if prof["href"].startswith("ShowRatings"):
            url_queue.put("http://www.ratemyprofessors.com/" + prof['href'])

'''
Returns a queue of URLs for professors' pages which can be found from the BASE_SCHOOL_URL
'''
def construct_URL_queue():
    url_queue = queue.Queue()
    prof_links_url = urlopen(BASE_SCHOOL_URL).read()
    prof_strainer = SoupStrainer(class_="profName")
    next_prof_links_html_strainer = SoupStrainer(id="pagination")
    while True:
        get_professor_links(BeautifulSoup(prof_links_url, parse_only=prof_strainer).findAll("a"), url_queue)
        next_prof_links_html = BeautifulSoup(prof_links_url, parse_only=next_prof_links_html_strainer).find(id="next")
        if next_prof_links_html:
            prof_links_url = urlopen("http://www.ratemyprofessors.com" + next_prof_links_html['href']).read()
        else: break
    return url_queue

'''
Returns a tuple of float data located in the professor's page's score card data
This tuple contains in order: 
Overall quality, Helpfulness, Clarity, and Easiness 
'''
def get_score_card_data(html):
    score_strainer = SoupStrainer(class_="tTip")
    score_card_html_soup = BeautifulSoup(html, parse_only=score_strainer)
    if not score_card_html_soup.find(id="quality"): 
        return 
    quality = float(score_card_html_soup.find(id="quality").find("strong").string)
    helpfulness = float(score_card_html_soup.find(id="helpfulness").find("strong").string)
    clarity = float(score_card_html_soup.find(id="clarity").find("strong").string)
    easiness = float(score_card_html_soup.find(id="easiness").find("strong").string)
    return quality, helpfulness, clarity, easiness
 
  
'''
Returns a string stating the average grade reported by students of the 
teacher who left ratings
'''
def get_grade(html):
    grade_strainer = SoupStrainer(id="rateNumber")
    strongs_html_soup = BeautifulSoup(html, parse_only=grade_strainer).findAll("strong") 
    #requires further searching to find strong tag containing letter_grade
    letter_grade = ''
    for spoon in strongs_html_soup:
        if spoon.string:
            results = re.findall('(N/A)|([ABCDF][+-]?)', spoon.string)
            # regex corresponds to N/A or any letter grade
            if len(results):
                for result in results[0]:
                    if result is not '':
                        letter_grade = result
    if letter_grade == '': #only for debugging purposes
        print(strongs_html_soup)
        print(get_name(html))
        raise AttributeError('failed to find grade')
    return letter_grade
  
'''
Returns the professor's hotness rating as an integer corresponding to the 
number of raters who believe the professor to be hot
'''
def get_hotness(html):
    hotness_strainer = SoupStrainer(id="scoreCard")
    hotness_html = BeautifulSoup(html, parse_only=hotness_strainer)
    hotness = int(re.findall("(?<=var status=)[^;]*", hotness_html.find(type="text/javascript").string)[0])
    # regex corresponds to variable initialization in javascript
    return hotness

'''
Returns the professors's name as a string
'''
def get_name(html):
    name_strainer = SoupStrainer("script", type="text/javascript")
    name_html_soup = BeautifulSoup(html, parse_only=name_strainer)
    name = ''
    for spoon in name_html_soup:
        if spoon.string:
            results = re.findall("(?<=prop7 : \")[^\";]*", spoon.string)
            # regex corresponds to variable initialization in javascript
            if len(results) and len(results[0]):
                name = results[0]
    
    return name

'''
Returns true if the professor has been rated
Necessary in the case of redirects to unrated pages
'''
def is_rated_professor(html):
    title_strainer = SoupStrainer("title")
    title_soup = BeautifulSoup(html, parse_only=title_strainer)
    for spoon in title_soup:
        if spoon.string:
            results = re.findall("(Add Rating)", spoon.string)
            if results:
                return False
    return True

'''
Returns a list of tuples containing the following information about a professor:
    Name(string), Score Card Data (float tuple 
    (Overall quality, Helpfulness, Clarity, and Easiness ) ), 
    Average Grade(string), Hotness(int), Ratings Page URL(string)
'''
def get_prof_list():
    url_queue = construct_URL_queue()
    prof_list = []
      
    while not url_queue.empty():
        professor_url = url_queue.get()
        professor_html = urlopen(professor_url).read()
        
        if not is_rated_professor(professor_html):
            continue
        
        name = get_name(professor_html)
        score_card_data = get_score_card_data(professor_html)
        grade = get_grade(professor_html)
        hotness = get_hotness(professor_html)
        
        course_data = ProfessorData(name, score_card_data, grade, hotness, professor_url)
        prof_list.append(course_data)
    return prof_list

if __name__ == '__main__':
    prof_list = get_prof_list()
        
    for prof_data in prof_list:
        print(prof_data + "\n")
  
'''
Returns a list of html for comments left on the professor's page
Currently unused, unprocessed and untested
Possible TODO: process comments for usable data
'''
def get_comments(professor_html):
    comment_strain = SoupStrainer(class_=re.compile("^entry (?=odd $|even $)"))
    # regex = "entry odd" or "entry even"
    comment_soup = BeautifulSoup(professor_html, parse_only=comment_strain)
    comments= []
    
    for spoon in comment_soup:
        comments.append(spoon.string)
        
    return comments