import pymysql

def pyConnect():
    connect = None
    try:
        connect = pymysql.connect(host='localhost', port=3306, user='root', database='msgapi', cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        print(e)
    return connect