'''
Created on Mar 2, 2014

@author: Sam Gegg
'''

class RateMyProfessorData(object):
    '''
    Stores the data pulled for a professor from ratemyprofessor.com
    '''


    def __init__(self, name, score_card_data, grade, hotness, url):
        '''
        Constructor
        first_name, last_name is exactly what you'd think
        quality, helpfulness, etc. data pulled from student evaluations on ratemyprofessor.com
        average_grade is average reported grade from professor's students
        '''
        split = name.split()
        self.first_name = split[0]
        self.last_name = split[-1]
        self.quality, self.helpfulness, self.clarity, self.easiness = score_card_data
        self.average_grade = grade
        self.hotness = hotness
        self.ratemyprofessor_url = url
        
    def __str__(self):
        self_str = self.last_name + ", " + self.first_name + "\n" 
        self_str += str(self.quality) + ", " + str(self.helpfulness) + ", " + str(self.clarity) + ", " + str(self.easiness) + "\n"
        self_str += str(self.average_grade) + "\n" 
        self_str += str(self.hotness) + "\n" 
        self_str += self.ratemyprofessor_url
        return self_str

    '''
    This function takes a Professor and returns a Document for mongoDB to use
    '''
    def dataToDoc(self):
        doc = {"first_name": self.first_name, "last_name": self.last_name, 
               "quality": self.quality, "helpfulness": self.helpfulness, "clarity": self.clarity, "easiness": self.easiness, 
               "grade": self.average_grade, "hotness": self.hotness, "ratemyprofessor_url": self.ratemyprofessor_url}
        return doc
