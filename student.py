# -*- coding: UTF-8 -*-
import sqlite3
import requests


def get_gp(score):
    score = float(score)

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


def get_push_list():
    ret_list = list()
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    res = cur.execute('SELECT sid, pwd, event_name, key FROM `student` WHERE pwd IS NOT NULL')
    for item in res:
        ret_list.append(item)
    conn.close()

    return ret_list


class Student:
    def __init__(self, sid, pwd):
        self.sid = sid
        self.pwd = pwd
        self.conn = sqlite3.connect('app.db')
        self.session = requests.Session()
        self.name = None
        self.college = None
        self.major = None
        self.event_name = None
        self.key = None

    def __del__(self):
        self.conn.close()

    def load_info(self):
        cur = self.conn.cursor()
        res = cur.execute('SELECT name, college, major, event_name, key FROM `student` WHERE sid=?', (self.sid,))
        for item in res:
            self.name = item[0]
            self.college = item[1]
            self.major = item[2]
            self.event_name = item[3]
            self.key = item[4]

    def update_info(self, name, college, major):
        cur = self.conn.cursor()
        cur.execute('SELECT 1 FROM `student` WHERE sid=?', (self.sid,))
        cur.fetchall()
        if cur.rowcount == 0:
            cur.execute('INSERT INTO `student` (sid, name, college, major) VALUES (?, ?, ?, ?)', (self.sid, name,
                        college, major))
        else:
            cur.execute('UPDATE `student` SET name=?, college=?, major=? WHERE sid=?', (name, college, major,
                        self.sid))
        self.conn.commit()

    def update_push(self, event_name, key):
        cur = self.conn.cursor()
        cur.execute('UPDATE `student` SET pwd=?, event_name=?, key=? WHERE sid=?', (self.pwd, event_name, key, self.sid))
        self.conn.commit()

    def update_grade(self, grade):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO `grade` (sid, cid, cnumber, cname, point, attr, grade) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (self.sid, grade[0], grade[1], grade[2], float(grade[3]), grade[4], grade[5]))
        self.conn.commit()

    def diff_grade(self, grade):
        cur = self.conn.cursor()
        cur.execute('SELECT grade FROM `grade` WHERE sid=? AND cid=?', (self.sid, grade[0]))
        if len(cur.fetchall()) == 0:
            return True

        return False

    def stop_push(self):
        cur = self.conn.cursor()
        cur.execute('UPDATE `student` SET pwd=NULL, event_name=NULL, key=NULL WHERE sid=?', (self.sid,))
        self.conn.commit()
