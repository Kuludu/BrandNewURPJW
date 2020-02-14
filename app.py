# -*- coding: UTF-8 -*-
import os
import pickle
from io import BytesIO
import pytesseract
from PIL import Image
from flask import Flask, render_template, request, make_response, session, redirect, url_for

import connect
import student

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('student') is None:
        session['student'] = pickle.dumps(student.Student())

    vis_student = pickle.loads(session['student'])

    if request.method == 'GET':
        if connect.test_login(vis_student):
            resp = redirect(url_for('manage'))
        else:
            session['login'] = 0
            resp = render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        vcode = request.form.get('vcode')

        if connect.login(vis_student, username, password, vcode):
            session['login'] = 1
            session['student'] = pickle.dumps(vis_student)
            resp = redirect(url_for('manage'))
        else:
            resp = make_response(render_template('error.html', message='用户名/密码/验证码错误，或教务系统挂了。'))

        if request.form.get('save'):
            resp.set_cookie('username', username)
            resp.set_cookie('password', password)
        else:
            resp.delete_cookie('username', username)
            resp.delete_cookie('password', password)

    return resp


@app.route('/manage', methods=['GET'])
def manage():
    resp = redirect(url_for('index'))

    if session.get('student') is not None:
        vis_student = pickle.loads(session['student'])
        if connect.test_login(vis_student):
            if vis_student.load() is False:
                return make_response(render_template('error.html', message="暂不支持等级制成绩"))
            resp = make_response(render_template('manage.html', stuff=vis_student))

    return resp


@app.route('/evaluation', methods=['GET', 'POST'])
def evaluation():
    if request.method == 'GET':
        return redirect(url_for('index'))

    resp = make_response(render_template('evaluation.html', status=0))

    if session.get('student') is not None:
        vis_student = pickle.loads(session['student'])
        if connect.test_login(vis_student):
            if vis_student.evaluate() is not False:
                resp = make_response(render_template('evaluation.html', status=1))

    return resp


@app.route('/vcode', methods=['GET'])
def vcode():
    if session.get('student') is None:
        session['student'] = pickle.dumps(student.Student())

    vis_student = pickle.loads(session['student'])
    checkcode = connect.get_vcode(vis_student)
    session['student'] = pickle.dumps(vis_student)

    if checkcode is False:
        resp = make_response(render_template('error.html', message="网络连接错误！"))
    else:
        resp = make_response(checkcode.content)
        img = Image.open(BytesIO(checkcode.content))

        optcode = pytesseract.image_to_string(img)
        optcode = filter(str.isalnum, optcode)
        optcode = ''.join(list(optcode))
        resp.set_cookie('vcode', optcode)

    return resp


@app.route('/logout', methods=['GET'])
def logout():
    if session.get('student') is not None:
        session.pop('student')
        session['login'] = 0

        resp = make_response(render_template('logout.html'))
    else:
        resp = redirect(url_for('index'))

    return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
