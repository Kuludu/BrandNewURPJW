# -*- coding: UTF-8 -*-
import os
from flask import Flask, render_template, make_response, session, redirect, url_for, request
from student import Student, get_gp
from fetch import login as stu_login
from fetch import fetch_exam, fetch_grade, fetch_info

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/', methods=['GET'])
def index():
    if session.get('student') is None:
        resp = redirect(url_for('login'))

    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    resp = render_template('error.html', message='应用内部错误！')
    if request.method == 'GET':
        if session.get('login') is None:
            return make_response(render_template('login.html'))
        else:
            return redirect(url_for('grade'))
    elif request.method == 'POST':
        sid = request.form.get('username')
        pwd = request.form.get('password')

        if sid is not None and pwd is not None:
            student = Student(sid, pwd)
            if stu_login(student):
                session['login'] = 1
                session['username'] = sid
                session['password'] = pwd

                student_info = fetch_info(student)
                student.update_info(student_info[0], student_info[1], student_info[2])

                resp = redirect(url_for('grade'))
            else:
                resp = make_response(render_template('error.html', message='用户名/密码/验证码识别错误，或教务系统挂了。'))

            if request.form.get('save'):
                resp.set_cookie('username', sid)
                resp.set_cookie('password', pwd)
            else:
                resp.delete_cookie('username', sid)
                resp.delete_cookie('password', pwd)

    return resp


@app.route('/grade', methods=['GET', 'POST'])
def grade():
    if session.get('login') is None:
        return redirect(url_for('login'))

    student = Student(session.get('username'), session.get('password'))
    if request.method == 'GET':
        stu_login(student)
        student.load_info()
        grades_info = fetch_grade(student)

        if grades_info is False:
            return make_response(render_template('error.html', message="应用内部错误"))

        courses = list()
        fails = list()
        pass_major = fail_major = pass_point = fail_point = gpa = ga = 0
        for grade_info in grades_info:
            try:
                float(grade_info[5])
            except ValueError:
                return make_response(render_template('error.html', message="暂不支持等级制成绩"))

            courses.append([grade_info[0], grade_info[1], grade_info[2], grade_info[3], grade_info[4], grade_info[5],
                           get_gp(grade_info[5])])
            if float(grade_info[5]) >= 60:
                pass_point += float(grade_info[3])
                if grade_info[4] != '任选':
                    pass_major += float(grade_info[3])
                    gpa += get_gp(grade_info[5]) * float(grade_info[3])
                    ga += float(grade_info[5]) * float(grade_info[3])
            else:
                fail_point += float(grade_info[3])
                if grade_info[4] != '任选':
                    fail_major += float(grade_info[3])
        gpa /= (pass_major + fail_major)
        ga /= (pass_major + fail_major)

        data = {
            'courses': courses,
            'fails': fails,
            'pass_point': pass_point,
            'fail_point': fail_point,
            'gpa': gpa,
            'ga': ga
        }

        resp = make_response(render_template('grade.html', student=student, data=data))
    elif request.method == 'POST':
        if request.form.get('reset') is not None:
            student.stop_push()
        else:
            event_name = request.form.get('event_name')
            key = request.form.get('key')
            student.update_push(event_name, key)

        resp = redirect(url_for('grade'))

    return resp


@app.route('/exam', methods=['GET'])
def exam():
    if session.get('login') is None:
        return redirect(url_for('login'))

    student = Student(session.get('username'), session.get('password'))
    stu_login(student)
    student.load_info()
    exams = fetch_exam(student)

    return render_template('exam.html', student=student, exams=exams)


@app.route('/logout', methods=['GET'])
def logout():
    if session.get('login'):
        session.pop('username')
        session.pop('password')
        session.pop('login')

        return make_response(render_template('logout.html'))

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
