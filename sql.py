import sqlite3
from sqlite3 import Error

def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def add_project(conn, project):
   """
   Create a new project into the projects table
   :param conn:
   :param project:
   :return: project id
   """
   sql = '''INSERT INTO projects(nazwa, start_date, end_date)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, project)
   return cur.lastrowid

def add_tasks(conn, task):
    """
    Create a new task into the tasks table
    :param conn:
    :param task:
    :return: task id
    """
    sql = '''INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
             VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid

def select_all(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()

   return rows

def select_where(conn, table, **query):
   """
   Query tasks from table with data from **query dict
   :param conn: the Connection object
   :param table: table name
   :param query: dict of attributes and values
   :return:
   """
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

def update(conn, table, id, **kwargs):
   """
   update status, begin_date, and end date of a task
   :param conn:
   :param table: table name
   :param id: row id
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

def delete(conn, table, id):

    sql = f"DELETE FROM {table} WHERE id=?"
    try:
       cur = conn.cursor()
       cur.execute(sql, (id,))
       conn.commit()
       print("Deleted")
    except sqlite3.OperationalError as e:
       print(e)

def delete_where(conn, table, **kwargs):
    
    qs = []
    values = tuple()
    for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")

project = ("Nauka ML", "2025-05-11 00:00:00", "2025-05-13 00:00:00")
task = ("2", "Nauka SQL'a", "Naucz się dodawać dane do tabeli", "started", "2025-05-11 00:00:00", "2025-05-13 00:00:00")

create_projects_sql = """
-- tworzymy tabelę projects
CREATE TABLE IF NOT EXISTS projects
(
   id          integer PRIMARY KEY,
   nazwa       text NOT NULL,
   start_date  text,
   end_date    text
);
"""
create_tasks_sql = """
-- tworzymy tabelę tasks
CREATE TABLE IF NOT EXISTS tasks
(
   id          integer PRIMARY KEY,
   project_id  integer NOT NULL,
   nazwa       VARCHAR(250) NOT NULL,
   opis        TEXT,
   status      VARCHAR(15) NOT NULL,
   start_date  text NOT NULL,
   end_date    text NOT NULL,
   FOREIGN KEY (project_id) REFERENCES projects (id)
);
"""
db_file = "database.db" #db_file name

if __name__ == '__main__':
    try:
        with sqlite3.connect(db_file) as conn:
            print(f"Success! Connected to {db_file}, sqlite version: {sqlite3.version}")
            #execute_sql(conn, create_projects_sql)
            #execute_sql(conn, create_tasks_sql)
            #add_project(conn, project)
            #add_tasks(conn, task)
            #print(select_all(conn, "projects"))
            #update(conn, "tasks", 2, status="ended")
            #print(select_where(conn, "tasks", id=1))
            #delete(conn, "projects", 3)
            delete_where(conn, "projects", id=3)
    except Error as e:
        print(e)