'''
Created on Mar 2, 2014

@author: Sam Gegg
'''

class KoofersCourseData(object):
    '''
    classdocs
    '''


    def __init__(self, gpa, prof_rating, grade_breakdown, course_id, url):
        '''
        Constructor
        subject_code is subject/department abbreviation e.g. CS, ATMS, etc.
        course_number is 3 digit number corresponding to course, e.g. 125, 428, etc.
        '''
        self.gpa = gpa
        self.prof_rating = prof_rating
        self.percent_A, self.percent_B, self.percent_C, self.percentD, self.percentF = grade_breakdown
        self.subject_code, self.course_number = course_id.split()
        self.koofers_url = url
        
    def __str__(self):
        self_str = str(self.gpa) + "\n"
        self_str += self.prof_rating + "\n"
        self_str += self.percent_A + ", " + self.percent_B + ", " + self.percent_C + ", " + self.percent_D + ", " + self.percent_F + "\n"
        self_str += self.subject_code + " " + self.course_number + "\n"
        self_str += self.url
        return self_str
        
    def dataToDoc(self):
        doc = {"gpa": self.gpa, "prof_rating": self.prof_rating, 
               "precentA": self.percentA, "precentB": self.percentB, "precentC": self.percentC, 
               "precentD": self.percentD, "precentF": self.percentF,
               "subject_code": self.subject_code, "course_number": self.course_number, 
               "koofers_url": self.koofers_url}
        return doc