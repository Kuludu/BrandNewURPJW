# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

import config

host = config.host
login_url = 'http://' + host + '/loginAction.do'
vcode_url = 'http://' + host + '/validateCodeAction.do'
name_url = 'http://' + host + '/xjInfoAction.do?oper=xjxx'
all_grade_url = 'http://' + host + '/gradeLnAllAction.do?type=ln&oper=fainfo'
exam_url = 'http://' + host + '/ksApCxAction.do?oper=getKsapXx'
eva_list_url = 'http://' + host + '/jxpgXsAction.do?oper=listWj'
eva_url = 'http://' + host + '/jxpgXsAction.do?oper=wjpg'


def test_login(student):
    try:
        res = student.session.post(name_url)
    except requests.exceptions.ConnectionError:
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
        res = student.session.post(login_url, data=form)
    except requests.exceptions.ConnectionError:
        return False

    dom = BeautifulSoup(res.text, 'html.parser')

    if dom.title.text == '学分制综合教务':
        return True
    else:
        return False


def evaluate(student, bpr, pgnr):
    form = {
        'wjbm': '0000000114',
        'bpr': bpr,
        'pgnr': pgnr,
        'xumanyzg': 'zg',
        'wjbz': '',
        '0000000042': '25_1',
        '0000000043': '10_1',
        '0000000044': '15_1',
        '0000000045': '25_1',
        '0000000046': '25_0.5',
        'zgpj': '老师很棒！'
    }

    try:
        resp = student.session.post(eva_url, data=form)
        return resp
    except requests.exceptions.ConnectionError:
        return False


def get_vcode(student):
    try:
        resp = student.session.post(vcode_url)
        return resp
    except requests.exceptions.ConnectionError:
        return False


def get_name_content(student):
    try:
        return student.session.get(name_url)
    except requests.exceptions.ConnectionError:
        return False


def get_all_grade_info_content(student):
    try:
        return student.session.get(all_grade_url)
    except requests.exceptions.ConnectionError:
        return False


def get_exam_content(student):
    try:
        return student.session.get(exam_url)
    except requests.exceptions.ConnectionError:
        return False


def get_eva_list(student):
    try:
        if test_login(student):
            return student.session.get(eva_list_url)
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False
