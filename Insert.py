import Connectionmodule, pymysql.cursors

connection = Connectionmodule.getConnection()

print("Connect successful!")

try:
    with connection.cursor() as cursor:
        # Create a new record
        cursor.execute("insert into customers values(NULL, 'admin@amrita.studio', 1234567890, 'admin', 'super', NOW(), NOW())")

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        cursor.execute('select * from customers')
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()