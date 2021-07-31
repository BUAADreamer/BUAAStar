import datetime

import pymysql


def register(name, password, login=True):
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db='bestconsumer')
    cursor = db.cursor()
    # print("connect to db")
    sql = "SELECT * FROM account \
           WHERE NAME = '%s'" % name
    if login:
        try:
            cursor.execute(sql)
            if cursor.rowcount > 0:
                result = cursor.fetchall()[0]
                db.close()
                if result[1] == password:
                    return 1
                else:
                    return 0
        except:
            return 0
    else:
        sql = "INSERT INTO account (name, password) VALUES (%s, %s)"
        val = (name, password)
        cursor.execute(sql, val)
        db.commit()
        db.close()
        return 1


def getHistoryData(name):
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db='bestconsumer')
    cursor = db.cursor()
    # print("connect to db")
    sql = "SELECT * FROM searchdata \
               WHERE USERNAME = '%s'" % name
    cursor.execute(sql)
    ret = []
    for x in cursor.fetchall():
        dic = {}
        dic['product'] = x[1]
        dic['date'] = x[2]
        dic['webname'] = x[3]
        dic['store'] = x[4]
        dic['productName'] = x[5]
        dic['price'] = x[6]
        dic['detailUrl'] = x[7]
        ret.append(dic)
    db.close()
    return ret


def addABlog(data, username):
    type = data['type']
    subtype = data['subtype']
    comment = data['comment']
    objectname = data['objectname']
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db='bestconsumer')
    cursor = db.cursor()
    sql = "INSERT INTO blog (username, type,subtype,comment,objectname,time,goodnum) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (username, type, subtype, comment, objectname, str(datetime.datetime.now()), 0)
    cursor.execute(sql, val)
    db.commit()
    db.close()


def createACourse(form):
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db='bestconsumer')
    cursor = db.cursor()
    sql = "INSERT INTO course (coursename,difficulty,worth,intro,smallname,coursetype,comments,academy,comnum,term) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (form['coursename'], form['difficulty'], form['worth'], form['intro'], form['smallname'],
           form['coursetype'], form['comments'], form['academy'], '1', form['term'])
    cursor.execute(sql, val)
    db.commit()
    db.close()


def getAllBlogs(type=""):
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db='bestconsumer')
    cursor = db.cursor()
    # print("connect to db")
    sql = "SELECT * FROM blog"
    cursor.execute(sql)
    ret = []
    for x in cursor.fetchall():
        dic = {}
        dic['username'] = x[0]
        dic['comment'] = x[1]
        dic['type'] = x[2]
        dic['subtype'] = x[3]
        dic['objectname'] = x[4]
        dic['isbegin'] = x[5]
        dic['goodnum'] = x[6]
        dic['time'] = x[7].strip()[:-10]
        ret.append(dic)
    ret = reversed(ret)
    db.close()
    return ret


def getCourseInfo(name):
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db='bestconsumer')
    cursor = db.cursor()
    # print("connect to db")
    sql = "SELECT coursename,difficulty,worth,intro,smallname,coursetype,comments,academy,comnum,term FROM course \
                   WHERE coursename = '%s'" % name
    cursor.execute(sql)
    dic = {}
    x = cursor.fetchone()
    print(x)
    dic['coursename'] = x[0]
    dic['difficulty'] = x[1]
    dic['worth'] = x[2]
    dic['intro'] = x[3]
    dic['smallname'] = x[4]
    dic['type'] = x[5]
    dic['comments'] = x[6].split('<sep>')
    dic['academy'] = x[7]
    dic['comnum'] = x[8]
    dic['term'] = x[9]
    print(dic)
    db.close()
    return dic


def getAllCourseInfo():
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db='bestconsumer')
    cursor = db.cursor()
    # print("connect to db")
    sql = "SELECT coursename,difficulty,worth,intro,smallname,coursetype,comments,academy,comnum,term FROM course "
    cursor.execute(sql)
    ls = []
    for x in cursor.fetchall():
        dic = {}
        dic['coursename'] = x[0]
        dic['difficulty'] = x[1]
        dic['worth'] = x[2]
        dic['intro'] = x[3]
        dic['smallname'] = x[4]
        dic['type'] = x[5]
        dic['comments'] = x[6].split('<sep>')
        dic['academy'] = x[7]
        dic['comnum'] = x[8]
        dic['term'] = x[9]
        ls.append(dic)
    db.close()
    return ls


def addCourseComment(form):
    coursename = form['coursename']
    print(form)
    difficulty = float(form['difficulty'])
    worth = float(form['worth'])
    comment = form['comment']
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db='bestconsumer')
    cursor = db.cursor()
    sql = "SELECT coursename,difficulty,worth,intro,smallname,coursetype,comments,academy,comnum FROM course \
                       WHERE coursename = '%s'" % coursename
    cursor.execute(sql)
    x = cursor.fetchone()
    preworth = float(x[2])
    precomnum = int(x[8])
    predifficulty = float(x[1])
    precomment = x[6]
    comnum = precomnum + 1
    difficulty = (predifficulty * precomnum + difficulty) / comnum
    worth = (preworth * precomnum + worth) / comnum
    comments = precomment + '<sep>' + comment
    sql = "UPDATE course set difficulty='%s', worth='%s',comments='%s',comnum='%s'\
                           WHERE coursename = '%s'" % (
        str(round(difficulty, 2)), str(round(worth, 2)), comments, str(comnum), coursename)
    cursor.execute(sql)
    db.commit()
    db.close()


def init():
    # 打开数据库连接
    db = pymysql.connect(host='localhost', user='root', password='1325muller', db="bestconsumer")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS ACCOUNT")

    # 使用预处理语句创建表
    sql = """CREATE TABLE ACCOUNT (
             NAME  CHAR(20) NOT NULL,
             PASSWORD CHAR(20) NOT NULL
             )"""

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    init()
