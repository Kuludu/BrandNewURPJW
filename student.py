# -*- coding: UTF-8 -*-
import sqlite3
import requests


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

    def __del__(self):
        self.conn.close()

    def update_info(self, name, college, major):
        cur = self.conn.cursor()
        cur.execute('SELECT 1 FROM `student` WHERE sid=?', (self.sid,))
        if len(cur.fetchall()) == 0:
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

    def load_push(self):
        cur = self.conn.cursor()
        res = cur.execute('SELECT event_name, key FROM student WHERE sid=?', (self.sid,))

        ret = dict()

        for item in res:
            ret['event_name'] = item[0]
            ret['key'] = item[1]

        return ret

    def stop_push(self):
        cur = self.conn.cursor()
        cur.execute('UPDATE `student` SET pwd=NULL, event_name=NULL, key=NULL WHERE sid=?', (self.sid,))
        self.conn.commit()
