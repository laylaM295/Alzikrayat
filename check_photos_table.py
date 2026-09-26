from app.core.database import getConnection


connection = getConnection()

try:
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE Photos")

        columns = cursor.fetchall()

        for column in columns:
            print(column)

finally:
    connection.close()