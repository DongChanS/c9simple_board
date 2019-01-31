from flask import Flask,render_template,request,redirect
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/create',methods=['POST'])
def create():
    title = request.form.get('title')
    content = request.form.get('content')
    query("INSERT","articles",title=title,content=content)
    return redirect("/")
    
@app.route('/page/<int:num>')
def page(num):
    res = query("SELECT","articles",string="LIMIT 10 OFFSET "+str(10*num))
    return render_template('page.html',res=res,num=num)
    
@app.route('/delete/<int:id_>/<num>')
def delete(id_,num):
    query("DELETE","articles",id_=id_)
    return redirect('/page/'+num)
    
@app.route('/edit/<int:id_>/<num>')
def edit(id_,num):
    c = sqlite3.connect('board.sqlite3')
    db = c.cursor()
    contents = db.execute('SELECT title,content FROM articles WHERE id = ?',(id_,)).fetchone()
    return render_template('edit.html',contents=contents,id_=id_,num=num)
    
@app.route('/edit_result',methods=['POST'])
def edit_result():
    title = request.form.get('title')
    content = request.form.get('content')
    id_ = request.form.get('id')
    num = request.form.get('num')
    query("UPDATE","articles",id_=id_,title=title,content=content)
    return redirect('/page/'+num)
    
def query(query,table,id_=None,string=None,**kwargs):
    c = sqlite3.connect('board.sqlite3')
    db = c.cursor()
    if query == "SELECT":
        if string:
            sql = "SELECT * FROM {} {}".format(table,string)
        else:
            sql = "SELECT * FROM {}".format(table)
        print(sql)
        return db.execute(sql).fetchall()
    elif query == "INSERT":
        keys = tuple(kwargs.keys())
        values = tuple(kwargs.values())
        sql = "INSERT INTO {} {} VALUES {}".format(table,keys,values)
    elif query == "DELETE":
        sql = "DELETE FROM {} WHERE id = {}".format(table,id_)
    elif query == "UPDATE":
        info = ""
        for key,value in kwargs.items():
            info += key + "='" + value +"',"
        sql = "UPDATE {} SET {} WHERE id = {}".format(table,info[:-1],id_)
    print(sql)
    db.execute(sql)
    c.commit()