import sqlite3
from flask import Flask, request, redirect, url_for
app = Flask(__name__)
with sqlite3.connect('up.db') as s:
    v = s.execute('select * from sqlite_master')
    if 'ss' not in [i[1] for i in v.fetchall()]:
        s.execute('create table ss(u string,p string)')
@app.route('/')
def up(method=['get']):
    if request.method=='GET':
        try:
            s,m = request.args['u'],request.args['p']
            if s != None and m != None:
                with sqlite3.connect('up.db') as db:
                    db.execute('insert into ss (u, p) values (?,?)',(s,m))
                return redirect(url_for('up'))
        except:
            pass
    s = sqlite3.connect('up.db').execute('select * from ss').fetchall()
    t='<form method ="get">\
        <input type="text" name="u" />\
        <input type="text" name="p" />\
        <input type ="submit" value="ok" /></form>'
    t+='<table border="1">'
    for i in s:
        t+='<tr><td>'+unicode(i[0])+'</td><td>'+unicode(i[1])+'</td></tr>'
    t+='<table>'
    return t.encode('utf-8')
if __name__ == '__main__':
    app.run()
