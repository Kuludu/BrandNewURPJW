# -*- coding: UTF-8 -*-
import json
import requests
import time
from student import get_push_list, Student
from fetch import fetch_grade, login

from config import MAX_RETRY_TIME, REFRESH_TIME

api_entery = 'https://maker.ifttt.com/trigger/%s/with/key/%s'


def push_grade(event_name, key, course_name, course_grade):
    data = {
        'value1': course_name,
        'value2': course_grade
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        res = requests.post(api_entery % (event_name, key), headers=headers, data=json.dumps(data))
    except requests.exceptions.ConnectionError:
        return False

    if res.status_code == 200:
        return True
    else:
        return False


def grade_watcher():
    push_list = get_push_list()

    for item in push_list:
        student = Student(item[0], item[1])
        if login(student) is False:
            continue
        student.load_info()

        grade_list = fetch_grade(student)
        if grade_list is False:
            continue
        for grade in grade_list:
            if student.diff_grade(grade):
                student.update_grade(grade)
                try_time = 0
                while try_time < MAX_RETRY_TIME:
                    if push_grade(student.event_name, student.key, grade[2], grade[5]):
                        break

                    try_time += 1
                    time.sleep(30)

    time.sleep(60 * REFRESH_TIME)


if __name__ == '__main__':
    while True:
        print("Watcher is running.")
        grade_watcher()
