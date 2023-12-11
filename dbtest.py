import psycopg2


class Databases:
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            dbname="test",
            user="postgres",
            password="mydbpassword",
        )
        self.cursor = self.db.cursor()  # 명령을 처리할 때 사용

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()


class CRUD(Databases):
    def insertDB(self, schema, table, column, data):
        print(data)
        placeholders = ", ".join(["%s" for _ in range(len(data[0]))])
        sql = " INSERT INTO {schema}.{table}({column}) VALUES ({placeholders})".format(
            schema=schema, table=table, column=column, placeholders=placeholders
        )
        try:
            self.cursor.executemany(sql, data)
            self.db.commit()
        except Exception as e:
            print("Insert Error", e)

    def readDB(self, schema, table, column):
        sql = " SELECT {column} from {schema}.{table}".format(
            column=column, schema=schema, table=table
        )
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            result = (" read DB err", e)
        return result

    def updateDB(self, schema, table, column, value, condition):
        sql = " UPDATE {shcema}.{table} SET {column}={value} WHERE {column}={condition}".format(
            schema=schema, table=table, column=column, value=value, condition=condition
        )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(" update DB error", e)

    def deleteDB(self, schema, table, condition):
        sql = " DELETE FROM {schema}.{table} where {condition}".format(
            schema=schema, table=table, condition=condition
        )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("DELETE DB err", e)


if __name__ == "__main__":
    str1 = 'ss"ss'
    str2 = "ssI'am"
    mixed_data = [(15, str2, True)]
    db = CRUD()
    print(db)
    db.insertDB(schema="public", table="test", column="int, str, bool", data=mixed_data)
