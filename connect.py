# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

import config

host = config.host
login_url = 'http://' + host + '/loginAction.do'
vcode_url = 'http://' + host + '/validateCodeAction.do'
name_url = 'http://' + host + '/xjInfoAction.do?oper=xjxx'
grade_url = 'http://' + host + '/gradeLnAllAction.do?type=ln&oper=qbinfo'

init_headers = {
    'Connection': 'Keep-Alive',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Just a cute spider!',
    'Accept-Encoding': 'gzip, deflate',
    'Host': host,
}


def test_login(student):
    try:
        res = student.session.post(name_url, headers=student.headers)
    except ConnectionError:
        return False

    dom = BeautifulSoup(res.text, 'html.parser')

    if dom.title.text == '学籍查询':
        return True
    else:
        return False


def login(student, username, password, vcode):
    form = {
        'zjh': username,
        'mm': password,
        'v_yzm': vcode
    }

    try:
        res = student.session.post(login_url, headers=student.headers, data=form)
    except ConnectionError:
        return False

    dom = BeautifulSoup(res.text, 'html.parser')

    if dom.title.text == '学分制综合教务':
        return True
    else:
        return False


def get_vcode(student):
    try:
        resp = student.session.post(vcode_url, headers=student.headers)
        return resp
    except ConnectionError:
        return False


def get_name_content(student):
    try:
        return student.session.get(name_url, headers=student.headers)
    except ConnectionError:
        return False


def get_gradeinfo_content(student):
    try:
        return student.session.get(grade_url, headers=student.headers)
    except ConnectionError:
        return False
