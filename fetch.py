# -*- coding: UTF-8 -*-
import muggle_ocr
import requests
from bs4 import BeautifulSoup

from config import HOST


def login(student):
    try:
        vcode_img = student.session.get('http://' + HOST + '/validateCodeAction.do').content
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        vcode = sdk.predict(image_bytes=vcode_img)
        data = {
            'zjh': student.sid,
            'mm': student.pwd,
            'v_yzm': vcode
        }

        res = student.session.post('http://' + HOST + '/loginAction.do', data=data)
        dom = BeautifulSoup(res.text, 'html.parser')

        if dom.title.text == '学分制综合教务':
            return True

        return False
    except requests.exceptions.RequestException:
        return False


def is_logined(student):
    try:
        res = student.session.get('http://' + HOST + '/xjInfoAction.do?oper=xjxx')
        dom = BeautifulSoup(res.text, 'html.parser')

        if dom.title.text == '学籍查询':
            return True

        return False
    except requests.exceptions.RequestException:
        return False


def fetch_grade(student):
    try:
        ret_grade = list()
        if is_logined(student) is False:
            return False

        res = student.session.get('http://' + HOST + '/gradeLnAllAction.do?type=ln&oper=fainfo')
        dom = BeautifulSoup(res.text, 'html.parser')
        courses_dom = dom.find_all('tr', class_='odd')
        for course_dom in courses_dom:
            cur_dom = BeautifulSoup(str(course_dom), 'html.parser')
            course_info = cur_dom.find_all('td')
            ret_grade.append([course_info[x].get_text().strip() for x in [0, 1, 2, 4, 5, 6]])

        return ret_grade
    except requests.exceptions.RequestException:
        return False


def fetch_info(student):
    try:
        if is_logined(student) is False:
            return False

        res = student.session.get('http://' + HOST + '/xjInfoAction.do?oper=xjxx')
        dom = BeautifulSoup(res.text, 'html.parser')
        info_dom = dom.find_all('td', width='275')

        name = info_dom[1].get_text().strip()
        college = info_dom[24].get_text().strip()
        major = info_dom[25].get_text().strip()

        return [name, college, major]
    except requests.exceptions.RequestException and IndexError:
        return False
