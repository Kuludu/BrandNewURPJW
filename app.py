# -*- coding: UTF-8 -*-
import os

from flask import Flask, session, request

from fetch import login as stu_login
from student import Student

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['VERSION'] = '2.1.0'


@app.route('/api/login', methods=['POST'])
def login():
    resp = {
        'status': "success"
    }

    sid = request.form.get('username')
    pwd = request.form.get('password')

    if sid is not None and pwd is not None:
        student = Student(sid, pwd)
        if stu_login(student):
            session['login'] = 1
            session['username'] = sid
            session['password'] = pwd
    else:
        resp['status'] = "failed"

    return resp


if __name__ == '__main__':
    app.run()
