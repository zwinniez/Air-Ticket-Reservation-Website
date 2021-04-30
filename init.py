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
	query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
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
	query = 'SELECT * FROM booking_agent WHERE email = %s and password = md5(%s) and booking_agent_ID = %s'
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
	query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'
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
		ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s,%s, %s, %s, %s, %s, %s, %s, %s)'
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
		ins = 'INSERT INTO booking_agent VALUES(%s, md5(%s), %s)'
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
		ins = 'INSERT INTO airline_staff VALUES(%s, md5(%s), %s, %s, %s)'
		cursor.execute(ins, (username, password, fname, lname, dob))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#home page for customer
@app.route('/home_customer')
def home_customer():
	email = session['email']
	cursor = conn.cursor();
	query = 'SELECT name, flight_num, departure_date_and_time, arrival_date_and_time, status \
		FROM purchase natural join reserve natural join flight WHERE c_email = %s'
	cursor.execute(query, (email))
	data1 = cursor.fetchall() 
	cursor.close()

	months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
	cursor = conn.cursor();
	query = "SELECT sum(sold_price) as total, purhcase_date_and_time as date FROM ticket natural join customer\
		 WHERE email = %s \
		GROUP BY purhcase_date_and_time" #fix mispelling in db
	cursor.execute(query, (email))
	data4= cursor.fetchall()
	cursor.close()
	labels = [each for each in months]
	values = [each['total'] for each in data4]
	colors = []

	return render_template('home_customer.html', email=email, flights=data1, \
		title="Your past year spendings", max=10000, labels=labels, values=values, \
			set=zip(values,labels, colors))

#search flights page 
@app.route('/flights')
def flights():
	email = session['email']
	departure_searches = session['departure_searches']
	return_searches = session['return_searches']
	return render_template('flights_customer.html', email=email, departure_searches=departure_searches,\
		return_searches = return_searches)

#search flights page for BA
@app.route('/flights_booking_agent')
def flights_booking_agent():
	email = session['email']
	departure_searches = session['departure_searches']
	return_searches = session['return_searches']
	return render_template('flights_booking_agent.html', email=email, departure_searches=departure_searches,\
		return_searches = return_searches)

@app.route('/flight_status')
def flight_status():
	email = session['email']
	statuses = session['statuses']
	return render_template('flight_status.html', email=email, statuses=statuses)

@app.route('/flight_status_booking_agent')
def flight_status_booking_agent():
	email = session['email']
	statuses = session['statuses']
	return render_template('flight_status_booking_agent.html', email=email, statuses=statuses)

@app.route('/search_status', methods=['GET', 'POST'])
def search_status():
	email = session['email']
	airline_name = request.form['airline_name'].lower()
	flight_num = request.form['flight_num']
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']
	cursor = conn.cursor();
	query = 'SELECT name, flight_num, status FROM flight WHERE\
		 name = %s and flight_num = %s and departure_date_and_time = %s \
		 	 and arrival_date_and_time = %s'
	cursor.execute(query, (airline_name, flight_num, departure_date, arrival_date))
	data3 = cursor.fetchall()
	cursor.close()
	session['statuses'] = data3
	return redirect(url_for('flight_status'))

@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
	email = session['email']
	print(request.form)
	departure = request.form['departure'].lower()
	arrival = request.form['arrival'].lower()
	departure_date = request.form['departure_date']
	return_date = request.form['return_date']
	cursor = conn.cursor();
	query = 'SELECT flight_num, departure_date_and_time FROM airport natural join arrival WHERE\
		 (name = %s or city = %s) and flight_num in \
			 (select flight_num FROM airport natural join departure where name = %s or city = %s)\
				 and departure_date_and_time = %s'
	cursor.execute(query, (departure, departure, arrival, arrival, departure_date))
	data2 = cursor.fetchall()
	cursor.close()
	session['departure_searches'] = data2
	if return_date is not None:
		cursor = conn.cursor();
		query = 'SELECT flight_num, departure_date_and_time FROM airport natural join arrival WHERE\
			(name = %s or city = %s) and flight_num in \
				(select flight_num FROM airport natural join departure where name = %s or city = %s)\
					and departure_date_and_time = %s'
		cursor.execute(query, (arrival, arrival, departure, departure, return_date))
		data2 = cursor.fetchall()
		cursor.close()
		session['return_searches'] = data2
	return redirect(url_for('flights'))

@app.route('/search_status_BA', methods=['GET', 'POST'])
def search_status_BA():
	email = session['email']
	airline_name = request.form['airline_name'].lower()
	flight_num = request.form['flight_num']
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']
	cursor = conn.cursor();
	query = 'SELECT name, flight_num, status FROM flight WHERE\
		 name = %s and flight_num = %s and departure_date_and_time = %s \
		 	 and arrival_date_and_time = %s'
	cursor.execute(query, (airline_name, flight_num, departure_date, arrival_date))
	data3 = cursor.fetchall()
	cursor.close()
	session['statuses'] = data3
	return redirect(url_for('flight_status_booking_agent'))

#searching for flights for BA
@app.route('/search_flights_BA', methods=['GET', 'POST'])
def search_flights_BA():
	email = session['email']
	print(request.form)
	departure = request.form['departure'].lower()
	arrival = request.form['arrival'].lower()
	departure_date = request.form['departure_date']
	return_date = request.form['return_date']
	cursor = conn.cursor();
	query = 'SELECT flight_num, departure_date_and_time FROM airport natural join arrival WHERE\
		 (name = %s or city = %s) and flight_num in \
			 (select flight_num FROM airport natural join departure where name = %s or city = %s)\
				 and departure_date_and_time = %s'
	cursor.execute(query, (departure, departure, arrival, arrival, departure_date))
	data2 = cursor.fetchall()
	cursor.close()
	session['departure_searches'] = data2
	if return_date is not None:
		cursor = conn.cursor();
		query = 'SELECT flight_num, departure_date_and_time FROM airport natural join arrival WHERE\
			(name = %s or city = %s) and flight_num in \
				(select flight_num FROM airport natural join departure where name = %s or city = %s)\
					and departure_date_and_time = %s'
		cursor.execute(query, (arrival, arrival, departure, departure, return_date))
		data2 = cursor.fetchall()
		cursor.close()
		session['return_searches'] = data2
	return redirect(url_for('flights_booking_agent'))

#home page for booking agent 
@app.route('/home_booking_agent')
def home_booking_agent():
	email = session['email']
	cursor = conn.cursor();
	query = 'SELECT name, flight_num, departure_date_and_time, arrival_date_and_time, status \
		FROM purchase natural join reserve natural join flight WHERE b_email = %s'
	cursor.execute(query, (email))
	data1 = cursor.fetchall() 
	cursor.close()
	return render_template('home_booking_agent.html', email=email, flights=data1)
	
'''
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
	session.pop('email')
	session.pop('departure_searches')
	session.pop('return_searches')
	session.pop('statuses')
	##logout all session variables TODO 
	return redirect('/')
	
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
