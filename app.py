from flask import Flask, render_template, send_from_directory, url_for, session, request
from account import *
from crawler import *
import os
import datetime
from drawPic import *

app = Flask(__name__, template_folder="./static",
            static_folder="./static",
            static_url_path="")
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def index():
    return render_template('sign-in.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('sign-up.html')
    else:
        name = request.form['name']
        password = request.form['password']
        if register(name, password, False) == 1:
            return render_template("sign-in.html")


@app.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("sign-in.html")
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if register(name, password) == 1:
            blogs = getAllBlogs()
            session['username'] = name
            return render_template("index.html", name=name, blogs=blogs)
        else:
            return render_template("sign-in.html")


@app.route('/index', methods=['GET', 'POST'])
def index1():
    if request.method == 'GET':
        blogs = getAllBlogs()
        name = session['username']
        return render_template("index.html", name=name, blogs=blogs)
    elif request.method == 'POST':
        name = session['username']
        addABlog(request.form, name)
        blogs = getAllBlogs()
        return render_template("index.html", name=name, blogs=blogs)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        name = session['username']
        return render_template("profile.html", name=name)
    elif request.method == 'POST':
        return


@app.route('/search', methods=['GET', 'POST'])
def searchProduct():
    if os.path.exists('./static/images/draw/hist.png'):
        os.remove("./static/images/draw/hist.png")
        os.remove('./static/images/draw/line.png')
    if request.method == 'GET':
        name = session['username']
        return render_template("searchproduct.html", name=name, infos={})
    elif request.method == 'POST':

        product = request.form['productName']
        name = session['username']
        productInfos, infos1 = getSpecContent(product)
        # print(productInfos)
        date = str(datetime.datetime.now()).split()[0]
        db = pymysql.connect(host='localhost', user='root', password='1325muller', db='bestconsumer')
        cursor = db.cursor()
        prils = []
        for info in infos1:
            prils.append(info['price'])
            sql = "INSERT INTO searchdata (username, product,date,webname,store,price,productName,detailUrl) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)"
            val = (
                name, product, date, info['webname'], info['store'], info['price'], info['productName'],
                info['detailUrl'])
            cursor.execute(sql, val)
        drawHist(prils)
        drawLine(prils)
        db.commit()
        db.close()
        return render_template("searchproduct.html", name=name, infos=infos1)


@app.route('/profile-edit', methods=['GET', 'POST'])
def profileEdit():
    if request.method == 'GET':
        name = session['username']
        return render_template("profile-edit.html", name=name)
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if register(name, password) == 1:
            session['username'] = name
            return render_template("index.html", name=name)
        else:
            return render_template("sign-in.html")


@app.route('/history', methods=['GET', 'POST'])
def getHistory():
    if request.method == 'GET':
        name = session['username']
        infos = getHistoryData(name)
        return render_template("history.html", name=name, infos=infos)
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if register(name, password) == 1:
            session['username'] = name
            return render_template("index.html", name=name)
        else:
            return render_template("sign-in.html")


@app.route('/course', methods=['GET', 'POST'])
def course():
    name = session['username']
    if request.method == 'GET':
        infoList = getAllCourseInfo()
        # print(infoList)
        return render_template("course.html", name=name, infoList=infoList)
    elif request.method == 'POST':
        infoList = getAllCourseInfo()
        addCourseComment(request.form)
        infoList = getAllCourseInfo()
        return render_template("course.html", name=name, infoList=infoList)


@app.route('/searchcourse', methods=['GET', 'POST'])
def searchcourse():
    name = session['username']
    if request.method == 'GET':
        return render_template("searchcourse.html", name=name, get=1)
    elif request.method == 'POST':
        name = request.form['coursename']
        info = getCourseInfo(name)
        # print(info)
        return render_template("searchcourse.html", name=name, info=info, get=0)


@app.route('/addcourse', methods=['POST'])
def addcourse():
    name = session['username']
    if request.method == 'POST':
        try:
            # print(request.form)
            createACourse(request.form)
        except:
            print("create fail")
        # print('11111111111')
        infoList = getAllCourseInfo()
        return render_template("course.html", name=name, infoList=infoList)


if __name__ == '__main__':
    app.run(debug=True)
