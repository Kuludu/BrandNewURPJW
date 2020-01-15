# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

import connect


def get_gp(score):
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

    def __get_course(self, content, course_amount, tot_point):
        cur_sum_point = cur_sum_score = 0
        cur_dom = BeautifulSoup(str(content), 'html.parser')
        tot_course = cur_dom.find_all('td', align='center')
        tot_course_info = []

        for i in range(0, course_amount):
            course_info = []
            course_info.append(''.join(tot_course[0 + i * 7].get_text().split()))
            course_info.append(''.join(tot_course[1 + i * 7].get_text().split()))
            course_info.append(''.join(tot_course[2 + i * 7].get_text().split()))
            course_info.append(float(''.join(tot_course[4 + i * 7].get_text().split())))
            course_info.append(''.join(tot_course[5 + i * 7].get_text().split()))
            course_info.append(float(''.join(tot_course[6 + i * 7].get_text().split())))
            course_info.append(get_gp(course_info[5]))

            type = course_info[4]
            if type == '必修' or type == '体育选修':
                cur_sum_point += course_info[3] * course_info[6]
                cur_sum_score += course_info[3] * course_info[5]
            else:
                tot_point -= course_info[3]

            tot_course_info.append(course_info)

        self.sum_gpa += cur_sum_point
        self.sum_point += tot_point

        try:
            return [cur_sum_point / tot_point, cur_sum_score / tot_point, tot_point, tot_course_info]
        except ZeroDivisionError:
            return [0, 0, 0, []]

    def __get_gradeinfo(self, res):
        dom = BeautifulSoup(res.text, 'html.parser')
        titles = dom.select('b')

        i = 0
        for title in titles:
            ret = []

            cur_dom = dom.find_all('table', class_='titleTop2')[i]
            cur_dom = BeautifulSoup(str(cur_dom), 'html.parser')
            tot_info = cur_dom.find(height='21').get_text()

            pass_info = [int(s) for s in tot_info.split() if s.isdigit()]
            tot_point = float(tot_info.split()[3])
            tot_course = int(tot_info.split()[5])
            pass_cource = int(tot_info.split()[7])

            gpa_info = self.__get_course(cur_dom, pass_info[1], tot_point)

            ret.append(title.text)
            ret.append(gpa_info[2])
            ret.append(tot_course)
            ret.append(pass_cource)
            ret.append(gpa_info[0])
            ret.append(gpa_info[1])
            ret.append(gpa_info[3])

            self.terms.append(ret)

            i += 1

        self.tot_gpa = self.sum_gpa / self.sum_point

    def load(self):
        self.__get_name(connect.get_name_content(self))
        self.__get_gradeinfo(connect.get_gradeinfo_content(self))

    def __init__(self):
        self.gpa = self.sum_gpa = self.sum_point = 0
        self.terms = []
        self.session = requests.Session()
        self.headers = connect.init_headers
