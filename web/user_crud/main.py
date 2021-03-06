import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
import random 
import uuid

# Git 

# Feature X

@app.route('/')
def hello():
	return 'Welcome to Flask'

@app.route('/add', methods=['POST'])
def add_user():
	try:
		_json = request.form
		_id = str(uuid.uuid1().hex)
		_name = _json['inputName']
		_email = _json['inputEmail']
		_contact = _json['contact']
		_address = _json['address']
		_profession = _json['profession']
		_age = _json['age']
		if request.method == 'POST':
			sql = "INSERT INTO user_db VALUES(%s, %s, %s, %s, %s, %s, %s)"
			data = (_id, _name, _email,_contact,_address,_profession,_age)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User '+ _name +' added successfully! Your user id is : '+_id )
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM user_db")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/<id>')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM user_db WHERE user_id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update', methods=['POST'])
def update_user():
	try:
		_json = request.form
		_id = _json['id']
		_email = _json['inputEmail']
		_name = "'"+_json['inputName']+"'" if _json['inputName'] else 'NULL'
		_contact = "'"+_json['contact']+"'" if _json['contact'] else 'NULL'
		_address = "'"+_json['address']+"'" if _json['address'] else 'NULL'
		_profession = "'"+_json['profession']+"'" if _json['profession'] else 'NULL'
		if _name and _email and request.method == 'POST':
			sql = 'UPDATE user_db SET user_name=COALESCE('+ _name +', user_name), contact=COALESCE('+ _contact +', contact), address=COALESCE('+ _address +', address), profession=COALESCE('+ _profession +', profession) WHERE user_id=%s and user_email=%s'
			data = (_id, _email)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql,data)
			conn.commit()
			resp = jsonify('User '+ _id +' updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM user_db WHERE user_id=%s", (id))
		conn.commit()
		resp = jsonify('User '+str(id)+ ' deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
		
if __name__ == "__main__":
    app.run()