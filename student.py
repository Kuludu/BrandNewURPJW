# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

import connect


def get_gp(score):
    score = float(score)

    if score >= 90:
        return 4.0
    elif 85 <= score < 90:
        return 3.7
    elif 82 <= score < 85:
        return 3.3
    elif 78 <= score < 82:
        return 3.0
    elif 75 <= score < 78:
        return 2.7
    elif 71 <= score < 75:
        return 2.3
    elif 66 <= score < 71:
        return 2.0
    elif 62 <= score < 66:
        return 1.7
    elif 60 <= score < 62:
        return 1.3
    else:
        return 0


class Student:
    def __get_name(self, res):
        dom = BeautifulSoup(res.text, 'html.parser')
        dom = dom.find_all('td', width='275')

        self.name = ''.join((dom[1].text + '(' + dom[0].text + ')').split())
        self.college = ''.join(dom[24].text.split())
        self.major = ''.join(dom[25].text.split())

    def __get_all_grade_info(self, res):
        dom = BeautifulSoup(res.text, 'html.parser')
        courses_dom = dom.find_all('tr', class_='odd')

        for course_dom in courses_dom:
            cur_dom = BeautifulSoup(str(course_dom), 'html.parser')
            course_info = cur_dom.find_all('td')

            self.courses.append([course_info[0].get_text(), course_info[1].get_text(), course_info[2].get_text(),
                                 course_info[4].get_text(), course_info[5].get_text(), float(course_info[6].get_text()),
                                 get_gp(course_info[6].get_text())])

            if float(course_info[6].get_text()) >= 60:
                self.pass_point += float(course_info[4].get_text())
            else:
                self.fails.append([course_info[0].get_text(), course_info[1].get_text(), course_info[2].get_text(),
                                   course_info[4].get_text(), course_info[5].get_text(), course_info[6].get_text()])
                self.fail_point += float(course_info[4].get_text())

            if course_info[5] == '任选':
                self.elective_point += float(course_info[4].get_text())
                continue

            self.sum_gp_with_weight += float(course_info[4].get_text()) * float(get_gp(course_info[6].get_text()))
            self.sum_grade_with_weight += float(course_info[4].get_text()) * float(course_info[6].get_text())

    def __get_exam_info(self, res):
        dom = BeautifulSoup(res.text, 'html.parser')
        exams_dom = dom.find_all('tr', class_='odd')

        for exam_dom in exams_dom:
            cur_dom = BeautifulSoup(str(exam_dom), 'html.parser')
            exam_info = cur_dom.find_all('td')

            self.exams.append([exam_info[2].get_text(), exam_info[3].get_text(), exam_info[4].get_text(), exam_info[5].
                              get_text(), exam_info[6].get_text(), exam_info[7].get_text()])

    def load(self):
        self.__get_name(connect.get_name_content(self))
        self.__get_all_grade_info(connect.get_all_grade_info_content(self))
        self.__get_exam_info(connect.get_exam_content(self))

        try:
            self.gpa = self.sum_gp_with_weight / (self.pass_point + self.fail_point - self.elective_point)
            self.ave_grade = self.sum_grade_with_weight / (self.pass_point + self.fail_point - self.elective_point)
        except ZeroDivisionError:
            self.gpa = self.ave_grade = 0
            
    def __init__(self):
        self.pass_point = 0
        self.fail_point = 0
        self.elective_point = 0
        self.sum_gp_with_weight = 0
        self.sum_grade_with_weight = 0
        self.gpa = 0
        self.ave_grade = 0
        self.courses = []
        self.exams = []
        self.fails = []
        self.session = requests.Session()
        self.headers = connect.init_headers
