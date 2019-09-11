import pymysql.cursors


# Функция возвращает connection.
def getConnection():
    # Вы можете изменить параметры соединения.
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='12345',
                                 db='study',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        connection.ping()
    except Exception:
        print("error! " + Exception)
        exit(1)

    return connection

