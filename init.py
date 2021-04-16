#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
					   port= 3306,
                       user='root',
                       #password='your_password',
                       db='air ticket reservation',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login for customer
@app.route('/login_customer')
def login_customer():
	return render_template('login_customer.html')

#Login for booking agent
@app.route('/login_booking_agent')
def login_booking_agent():
	return render_template('login_booking_agent.html')

#Login for airline staff
@app.route('/login_airline_staff')
def login_airline_staff():
	return render_template('login_airline_staff.html')

#Define route for register customer
@app.route('/register_customer')
def register_customer():
	return render_template('register_customer.html')

#Define route for register for booking agent
@app.route('/register_booking_agent')
def register_booking_agent():
	return render_template('register_booking_agent.html')

#Define route for register for airline staff
@app.route('/register_airline_staff')
def register_airline_staff():
	return render_template('register_airline_staff.html')

#Authenticates the login for customer 
@app.route('/loginAuth_customer', methods=['GET', 'POST'])
def loginAuth_customer():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s and password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = email
		return redirect(url_for('home_customer'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or email'
		return render_template('login_customer.html', error=error)

#Authenticates the login for booking agent
@app.route('/loginAuth_booking_agent', methods=['GET', 'POST'])
def loginAuth_booking_agent():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	ID = request.form['booking_agent_ID']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s and booking_agent_ID = %s'
	cursor.execute(query, (email, password, ID))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = email
		return redirect(url_for('home_booking_agent'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login_booking_agent.html', error=error)

#Authenticates the login for airline staff
@app.route('/loginAuth_airline_staff', methods=['GET', 'POST'])
def loginAuth_airline_staff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home_airline_staff'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login_airline_staff.html', error=error)

#Authenticates the register
@app.route('/registerAuth_customer', methods=['GET', 'POST'])
def registerAuth_customer():
	#grabs information from the forms
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	dob = request.form['date_of_birth']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_customer.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, name, password, building_number, street, city, state, phone, passport_number,\
			passport_expiration, passport_country, dob))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Authenticates the register
@app.route('/registerAuth_booking_agent', methods=['GET', 'POST'])
def registerAuth_booking_agent():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	ID = request.form['booking_agent_ID']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_booking_agent.html', error = error)
	else:
		ins = 'INSERT INTO booking_agent VALUES(%s, %s, %s)'
		cursor.execute(ins, (email, password, ID))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Authenticates the register
@app.route('/registerAuth_airline_staff', methods=['GET', 'POST'])
def registerAuth_airline_staff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	fname = request.form['first_name']
	lname = request.form['last_name']
	dob = request.form['date_of_birth']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register_airline_staff.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, %s,%s, %s,%s)'
		cursor.execute(ins, (username, password, fname, lname, dob))
		conn.commit()
		cursor.close()
		return render_template('index.html')

'''
#home page for customer
@app.route('/home_customer')
def home_customer():
    #email = session['email']
    #cursor = conn.cursor();
    #query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    #cursor.execute(query, (username))
    #data1 = cursor.fetchall() 
    # for each in data1:
    #     print(each['blog_post'])
    # cursor.close()
    return render_template('home_customer.html', email=email)#, posts=data1)

#home page for booking agent 
@app.route('/home_booking_agent')
def home_booking_agent():
    
    #username = session['username']
    #cursor = conn.cursor();
    #query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    #cursor.execute(query, (username))
    #data1 = cursor.fetchall() 
    #for each in data1:
    #    print(each['blog_post'])
    #cursor.close()
    return render_template('home_booking_agent.html', username=username, posts=data1)

#home page for airline staff
@app.route('/home_airline_staff')
def home_airline_staff():
    
    #username = session['username']
    #cursor = conn.cursor();
    #query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    #cursor.execute(query, (username))
    #data1 = cursor.fetchall() 
    #for each in data1:
    #    print(each['blog_post'])
    #cursor.close()
    return render_template('home_airline_staff.html', username=username, posts=data1)
		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))
'''
@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
	
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
