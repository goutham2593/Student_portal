#!/usr/bin/python3

# standard library
import sqlite3 as sql

# python3 -m pip install flask
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# Main page
@app.route('/')
def home():
    return viewall()

@app.route('/addrecord')
def addrender():
    return render_template('add.html', msg = "Add your company to yellow pages")

@app.route('/addrecord',methods = ['POST'])
def addrecord():
    try:
        cname = request.form['cname']         # company name
        cphone = request.form['cphone']     # company phone
        cemail = request.form['cemail']     # company email
        caddress = request.form['caddress'] # company address
        # Database connectivity
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO yellowp (cname,cphone, cemail, caddress) VALUES (?,?,?,?)",(cname,cphone,cemail,caddress))
        # Execute
        con.commit()
    except Exception as e:
        print(e)
    finally:
        return render_template('add.html', msg = "Company record successfully added. Thank you!")

@app.route('/viewall')
def viewall():
    try:
        # Database connectivity
        with sql.connect("database.db") as con:
            cur = con.cursor()
            # Query
            cmp = cur.execute("SELECT * FROM yellowp").fetchall()
            # Execute
            con.commit()
    except Exception as e:
        print("Error: ",e)
    finally:
        return render_template('index.html', companies = cmp, msg="Welcome to Simple Yellow Pages")

@app.route('/updaterecord')
def updaterecord():
    try:
        # Database connectivity
        with sql.connect("database.db") as con:
            cur = con.cursor()
            # Query
            cmp = cur.execute("SELECT * FROM yellowp").fetchall()
            # Execute
            con.commit()
    except Exception as e:
        print("Error: ",e)
    finally:
        return render_template('update.html', companies = cmp, msg="Welcome to Simple Yellow Pages")

@app.route('/updaterecord', methods=['POST'])
def updaterec():
    print("here in update")
    try:
        cid = request.form['cid']      #companyid
        print(cid)
        cname = request.form['cname']         # company name
        cphone = request.form['cphone']     # company phone
        cemail = request.form['cemail']     # company email
        caddress = request.form['caddress'] # company address
        # Database connectivity
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE yellowp SET cname = ?, cphone = ?, cemail = ?,  caddress = ? WHERE id=?",(cname,cphone,cemail,caddress,cid))
        # Execute
        con.commit()
    except Exception as e:
        print(e)
    finally:
        return viewall()


@app.route('/viewall/', methods=['GET'])
def delrecord():
    cid = request.args.get('cid', '')
    try:
        # Database connectivity
        with sql.connect("database.db") as con:
            cur = con.cursor()
            # Query
            cur.execute("DELETE FROM yellowp WHERE id=?",(cid))
            # Execute
            con.commit()
    except Exception as e:
        print("Error: ",e)
    finally:
        return viewall()


if __name__ == '__main__':
    try:
        # ensure the sqliteDB is created
        con = sql.connect('database.db')
        print("Database connectivity is OK")
        con.execute('DROP TABLE yellowp')
        con.execute('CREATE TABLE IF NOT EXISTS yellowp (id INTEGER PRIMARY KEY AUTOINCREMENT,cname TEXT, cphone TEXT, cemail TEXT, \
                    caddress TEXT)')
        print("Table created successfully")
        con.close()
        # begin Flask Application 
        app.run(host="0.0.0.0", port=2224, debug = False)
    except:
        print("Error Running application")

