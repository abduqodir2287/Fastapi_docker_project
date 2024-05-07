import psycopg2

class Itmed_db:
    def __init__(self, dbname='tech.db'):
        self.dbname = dbname
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = psycopg2.connect(
            password="password", user="abduqodir",
            host="fastapi_db", port=5432, dbname="fastapi"
        )
        self.cur = self.conn.cursor()

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def create_table_org(self, tabname='organization'):
        sql_create_table = f"""
            CREATE TABLE IF NOT EXISTS {tabname}(
                id SERIAL PRIMARY KEY ,
                "org_name" TEXT
            );"""
        self.cur.execute(sql_create_table)
        self.conn.commit()

    def create_table_doc(self, tabname='doctors'):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {tabname}(
                id SERIAL PRIMARY KEY,
                firstname TEXT,
                lastname TEXT,
                age INTEGER,
                org_id INTEGER REFERENCES organization (id),
                org_name TEXT
            );"""
        self.cur.execute(sql)
        self.conn.commit()

    def create_table_patient(self, tabname='patient'):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {tabname}(
                id SERIAL PRIMARY KEY,
                firstname TEXT,
                lastname TEXT,
                age INTEGER,
                org_id INTEGER REFERENCES organization (id),
                org_name TEXT, 
                doctor_id INT REFERENCES doctors (id)
            );"""
        self.cur.execute(sql)
        self.conn.commit()

    def add_item_doc(
            self, firstname: str,
            lastname: str, age: int, org_id: int,
            org_name: str, table: str = "doctors"
    ):
        sql = f"""INSERT INTO "{table}" ("firstname", "lastname", "age", "org_id", org_name)
            VALUES (%s, %s, %s, %s, %s);"""
        data = (firstname, lastname, age, org_id, org_name)
        try:
            self.connect()
            self.cur.execute(sql, data)
            self.conn.commit()
        except psycopg2.errors.ForeignKeyViolation:
            print("Failed to")
            return "Organization not found"

    def add_item_org(self, org_name: str, table: str = "organization"):
        sql = f"""INSERT INTO "{table}" ("org_name")
            VALUES (%s);"""
        data = (org_name,)
        self.cur.execute(sql, data)
        self.conn.commit()

    def add_item_patient(
            self, firstname: str,
            lastname: str, age: int, org_id: int,
            org_name: str, doctor_id: int, table: str = "patient"
    ):
        sql = f"""INSERT INTO "{table}" ("firstname", "lastname", "age", "org_id", "org_name", "doctor_id")
            VALUES (%s, %s, %s, %s, %s, %s);"""
        data = (firstname, lastname, age, org_id, org_name, doctor_id)
        try:
            self.connect()
            self.cur.execute(sql, data)
            self.conn.commit()
        except psycopg2.errors.ForeignKeyViolation:
            print("Failed to")
            return "Organization or doctor not found"

    def delete_item_doc(self, id, table: str = "doctors"):
        sql = f"""DELETE FROM {table} where id = %s;"""
        self.cur.execute(sql, (id,))
        self.conn.commit()

    def delete_item_org_doc(self, org_id, table: str = "doctors"):
        sql = f"""DELETE FROM {table} where org_id = %s;"""
        self.cur.execute(sql, (org_id,))
        self.conn.commit()

    def delete_item_org(self, id, table: str = "organization"):
        sql = f"""DELETE FROM {table} where id = %s;"""
        self.cur.execute(sql, (id,))
        self.conn.commit()

    def delete_item_patient(self, id, table: str = "patient"):
        sql = f"""DELETE FROM {table} where id = %s;"""
        self.cur.execute(sql, (id,))
        self.conn.commit()

    def delete_item_org_patient(self, org_id, table: str = "patient"):
        sql = f"""DELETE FROM {table} where org_id = %s;"""
        self.cur.execute(sql, (org_id,))
        self.conn.commit()

    def delete_item_doc_patient(self, org_id, table: str = "patient"):
        sql = f"""DELETE FROM {table} where org_id = %s;"""
        self.cur.execute(sql, (org_id,))
        self.conn.commit()

    def select_item_org(self, table: str = "organization"):
        sql = f"""SELECT org.id AS org_id, org.org_name AS org_name,
                         array_agg(
                         doc.firstname || ' ' || doc.lastname || ' ' || doc.age || ' ' || doc.org_name
                         ) AS doctors
                  FROM {table} org
                  LEFT JOIN doctors doc
                      ON org.org_name = doc.org_name AND org.id = doc.org_id
                  GROUP BY org.id, org.org_name;"""
        self.connect()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def select_item_doc(self, table: str = "doctors"):
        sql = f"""SELECT * FROM {table};"""
        self.cur.execute(sql)
        return self.cur.fetchall()

    def select_item_patient(self, table: str = "patient"):
        sql = f"""SELECT * FROM {table};"""
        self.cur.execute(sql)
        return self.cur.fetchall()

    def select_item_inner(self, table: str = "organization"):
        sql = f"""
        SELECT * FROM {table} 
        INNER JOIN doctors ON {table}.id = doctors.org_id
        ;"""
        self.cur.execute(sql)
        return self.cur.fetchall()

    def update_item_doc(
            self, id: int, firstname: str,
            lastname: str, age: int,
            org_id: int, org_name: str,
            table: str = "doctors"
    ):
        sql = f"""UPDATE {table} SET
                "firstname" = %s,
                "lastname" = %s,
                "age" = %s,
                "org_id" = %s,
                "org_name" = %s
                WHERE id = %s;"""
        data = (firstname, lastname, age, org_id, org_name, id)
        self.cur.execute(sql, data)
        self.conn.commit()

    def update_item_patient(
            self, id: int, firstname: str,
            lastname: str, age: int,
            org_id: int, org_name: str,
            doctor_id: int, table: str = "patient"
    ):
        sql = f"""UPDATE {table} SET
                "firstname" = %s,
                "lastname" = %s,
                "age" = %s,
                "org_id" = %s,
                "org_name" = %s,
                "doctor_id" = %s
                WHERE id = %s;"""
        data = (firstname, lastname, age, org_id, org_name, doctor_id, id)
        self.cur.execute(sql, data)
        self.conn.commit()


    def update_item_org_doc(
            self, org_id: int, org_name: str,
            id: int, table: str = "doctors"
    ):
        sql = f"""UPDATE {table} SET
                "org_id" = %s,
                "org_name" = %s
                WHERE org_id = %s;"""
        data = (org_id, org_name, id)
        self.cur.execute(sql, data)
        self.conn.commit()

    def update_item_org_patient(
            self, org_id: int, org_name: str,
            id: int, table: str = "patient"
    ):
        sql = f"""UPDATE {table} SET
                "org_id" = %s,
                "org_name" = %s
                WHERE org_id = %s;"""
        data = (org_id, org_name, id)
        self.cur.execute(sql, data)
        self.conn.commit()


    def update_item_org(self, id: int, org_name: str, table: str = "organization"):
        sql = f"""UPDATE {table} SET
                "org_name" = %s
                WHERE id = %s;"""
        data = (org_name, id)
        self.cur.execute(sql, data)
        self.conn.commit()

    def log_out(self):
        self.cur.close()
        self.conn.close()

