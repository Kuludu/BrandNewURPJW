# -*- coding: UTF-8 -*-
import json
import requests
import time
import logging
from student import get_push_list, Student
from fetch import fetch_grade, login

from config import MAX_RETRY_TIME, REFRESH_TIME

api_entery = 'https://maker.ifttt.com/trigger/%s/with/key/%s'


def push_grade(event_name, key, course_name, course_grade):
    logging.info('Start pushing.')

    data = {
        'value1': course_name,
        'value2': course_grade
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        res = requests.post(api_entery % (event_name, key), headers=headers, data=json.dumps(data))
    except requests.exceptions.RequestException:
        logging.error('Push failed.')
        return False

    if res.status_code == 200:
        logging.error('Push success.')
        return True
    else:
        logging.error('Push failed.')
        return False


def grade_watcher():
    logging.info('Start pulling.')

    push_list = get_push_list()

    for item in push_list:
        student = Student(item[0], item[1])
        if login(student) is False:
            continue
        push_info = student.load_push()

        grade_list = fetch_grade(student)
        if grade_list is False:
            continue
        for grade in grade_list:
            if student.diff_grade(grade):
                student.update_grade(grade)
                try_time = 0
                while try_time < MAX_RETRY_TIME:
                    if push_grade(push_info['event_name'], push_info['key'], grade[2], grade[5]):
                        break

                    try_time += 1
                    time.sleep(60)

    time.sleep(60 * REFRESH_TIME)


if __name__ == '__main__':
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='bnurp_push.log', level=logging.INFO, format=LOG_FORMAT)

    while True:
        print("Watcher is running.")
        grade_watcher()
