import Connectionmodule, pymysql.cursors

connection = Connectionmodule.getConnection()

print("Connect successful!")

try:
    with connection.cursor() as cursor:
        # Create a new record
        cursor.execute("UPDATE customers SET pass = '21422142', latssd = NOW() WHERE unit_id = 1")

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