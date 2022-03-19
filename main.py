from flask import Flask, render_template
import util

app = Flask(__name__)

username='braxtonchambers'
password='1221'  
host='127.0.0.1'
port='5432'
database='dvdrental'

@app.route('/')
def index():
    # Connects to Database
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    # Executes SQL Commands
    record = util.run_and_fetch_sql(cursor,"Select fruit_a, fruit_b from basket_a, basket_b;")
    if record == -1:
        print('Something is wrong with the SQL command')
    else:
        # Returns All Column Names Selected
        col_names = [desc[0] for desc in cursor.description]
        # First 5 Rows
        log = record[:5]
    # Disconnects from Database
    util.disconnect_from_db(connection,cursor)
    # Searches for file 'index.html'
    return render_template('index.html', sql_table = log, table_title=col_names)


@app.route("/api/update_basket_a")
def update():
    # Connects to Database
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    # Executes SQL Commands
    record = util.run_and_commit_sql(cursor,connection, "INSERT INTO basket_a (a, fruit_a)VALUES (5, 'Cherry');")
    if record == -1:
        print('Something is wrong with the SQL command')
    else:
        log = 'Success'
        connection.commit()
        
    # Disconnects from Database
    util.disconnect_from_db(connection,cursor)
    return render_template('api/update_basket_a.html', log_html = log)


@app.route("/api/unique")
def unique():
    # Connects to Database
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    # Executes SQL Commands
    record = util.run_and_fetch_sql(cursor, "select fruit_a, fruit_b from basket_a Full Outer Join basket_b on basket_a.fruit_a=basket_b.fruit_b Where basket_a.a is NULL or basket_b.b is Null")
    
    if record == -1:
        print('Something is wrong with the SQL command')
    else:
        connection.commit()
        col_names = [desc[0] for desc in cursor.description]
        # First 5 Rows
        log = record[:5]
        # Disconnects from Database
        util.disconnect_from_db(connection,cursor)
        # Searches for file 'index.html'
        return render_template('api/unique.html', sql_table = log, table_title=col_names)


if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)