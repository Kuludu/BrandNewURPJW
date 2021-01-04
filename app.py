# -*- coding: UTF-8 -*-
import json
import os

from flask import Flask, session, request
from flask_cors import CORS

from fetch import login as stu_login, fetch_info, fetch_grade
from student import Student
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['VERSION'] = '2.1.0'
CORS(app, supports_credenntials=True)


@app.route('/api/login', methods=['POST'])
def login():
    resp = {
        'status': 'failed'
    }

    sid = request.form.get('username')
    pwd = request.form.get('password')

    if sid and pwd:
        student = Student(sid, pwd)
        if stu_login(student):
            resp['status'] = 'success'
            serializer = Serializer(app.config['SECRET_KEY'], expires_in=3600)
            token = serializer.dumps({'username': sid, 'password': pwd}).decode('utf8')
            resp['token'] = token

    # TODO Response code
    return json.dumps(resp)


@app.route('/api/logout', methods=['POST'])
def logout():
    resp = {
        'status': 'success'
    }

    if session.get('login'):
        session.pop('username')
        session.pop('password')
        session.pop('login')

    return json.dumps(resp)


@app.route('/api/info', methods=['POST'])
def info():
    resp = {
        'status': 'failed'
    }
    success = 0

    if request.form.get('token'):
        token = request.form.get('token')
        serializer = Serializer(app.config["SECRET_KEY"])
        try:
            user = serializer.loads(token)

            student = Student(user['username'], user['password'])
            stu_login(student)

            student_info = fetch_info(student)
            if student_info:
                success += 1
                resp['name'] = student_info[0]
                resp['college'] = student_info[1]
                resp['major'] = student_info[2]
                student.update_info(student_info[0], student_info[1], student_info[2])

            student_grades = fetch_grade(student)
            if student_grades:
                success += 1
                ret_grade = list()
                for student_grade in student_grades:
                    cur_grade = dict()
                    cur_grade['course_number'] = student_grade[0]
                    cur_grade['course_order_number'] = student_grade[1]
                    cur_grade['course_name'] = student_grade[2]
                    cur_grade['credit'] = student_grade[3]
                    cur_grade['course_attribute'] = student_grade[4]
                    cur_grade['course_grade'] = student_grade[5]

                    ret_grade.append(cur_grade)

                resp['grades'] = ret_grade
        except BadSignature:
            resp['desc'] = 'Bad token.'

        if success == 2:
            resp['status'] = 'success'

    return json.dumps(resp)


@app.route('/api/push', methods=['POST'])
def push():
    resp = {
        'status': 'failed'
    }

    if request.form.get('token'):
        token = request.form.get('token')
        serializer = Serializer(app.config["SECRET_KEY"])
        try:
            user = serializer.loads(token)

            student = Student(user['username'], user['password'])
            if stu_login(student):
                resp['status'] = 'success'
                event_name = request.form.get('event_name')
                key = request.form.get('event_name')

                if event_name and key:
                    student.update_push(event_name, key)
                else:
                    student.stop_push()

        except BadSignature:
            resp['desc'] = 'Bad token.'

    return json.dumps(resp)


if __name__ == '__main__':
    app.run()
