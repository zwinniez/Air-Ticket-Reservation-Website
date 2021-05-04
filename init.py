#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import json

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
					   port= 3306,
                       user='root',
                       #password='your_password',
                       db='air ticket',
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
		session['ID'] = ID
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

#comment/rate function for CUSTOMER 
@app.route('/rate_flight_C', methods=["GET", "POST"])
def rate_flight_C():
	email = session['email']
	flight_num = request.form['flight_num']
	departure_date_and_time = request.form['departure_date_and_time']
	return render_template('rate_flight_customer.html', email=email, flight_num=flight_num, \
		departure_date_and_time=departure_date_and_time)

#insert comment/rate for CUSTOMER to database and return to home customer
@app.route('/inserting_rate_C', methods=["GET", "POST"])
def inserting_rate_C():
	email = session['email']
	flight_num = request.form['flight_num']
	departure_date_and_time = request.form['departure_date_and_time']
	rating = request.form['rating']
	comment = request.form['comment']
	print(departure_date_and_time, "HI"*100)
	print(flight_num, departure_date_and_time, rating, comment, "HI"*20)
	cursor = conn.cursor()
	query = "INSERT INTO rating values(%s, %s, %s, %s, %s)"
	cursor.execute(query, (email, flight_num, departure_date_and_time, rating, comment))
	conn.commit()
	cursor.close()
	return redirect(url_for("confirmed_rating_C"))

#confirmation page for rating/commenting on past flight CUSTOMER USER
@app.route('/confirmed_rating_C')
def confirmed_rating_C():
	email = session['email']
	return render_template("confirmed_rating_customer.html", email=email)

#home page for CUSTOMER
@app.route('/home_customer')
def home_customer():
	email = session['email']
	# ---------------------------------------display purchased tickets-------------------------------
	cursor = conn.cursor()
	query = 'SELECT name, flight_num, departure_date_and_time, arrival_date_and_time, status \
		FROM purchase natural join reserve natural join flight WHERE c_email = %s and \
			departure_date_and_time - (select now()) > 0'
	cursor.execute(query, (email))
	data1 = cursor.fetchall()
	cursor.close()

	# ---------------------------------------display past flights and comments ------------------------
	cursor = conn.cursor()
	query = 'SELECT name, flight_num, departure_date_and_time, arrival_date_and_time, status \
		FROM purchase natural join reserve natural join flight WHERE c_email = %s and \
			arrival_date_and_time - (select now()) <= 0'
	cursor.execute(query, (email))
	data2 = cursor.fetchall()
	cursor.close()

	# ----------------------------------purchase history bar graph---------------------------------------
	months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
	labels = [each for each in months]
	values = [0 for i in range(12)]
	total = 0
	colors = []
	if 'prices' not in session: #default bar graph
		cursor = conn.cursor()
		query = "SELECT sold_price as price, purhcase_date_and_time as date FROM ticket natural join customer\
			WHERE email = %s and (select now()) - purhcase_date_and_time > 1" #fix mispelling in db
		cursor.execute(query, (email))
		data4= cursor.fetchall()
		cursor.close()
		#data4 is a list of dictionaries
		#each result is a dicitonary with attributes as keys 
		for i in range(12):
			for each in data4:
				if each['date'].month == i+1: 
					values[i] += each['price']
					total += each['price']
	else: #with custom range
		prices = session['prices'].strip().split(' ')
		dates = session['dates'].strip(',').split(',')
		for i in range(12):
			for j in range(len(prices)):
				date = dates[j].split()[0]
				month = int(date.split("-")[1])
				if month == i+1:
					values[i] += float(prices[j])
					total += float(prices[j])
	# -------------------------------------------------bar graph---------------------------------------

	return render_template('home_customer.html', email=email, flights=data1, past_flights=data2, \
		title="Summary of past spendings", max=10000, labels=labels, values=values, \
			total=total, set=zip(values,labels, colors), default_range="past year")

#home page for booking agent 
@app.route('/home_booking_agent')
def home_booking_agent():
	email = session['email']
	ID = session['ID']
	# ---------------------------------------display purchased tickets-----------------------------------------
	cursor = conn.cursor()
	query = 'SELECT name, flight_num, departure_date_and_time, arrival_date_and_time, status \
		FROM purchase natural join reserve natural join flight WHERE b_email = %s'
	cursor.execute(query, (email))
	data1 = cursor.fetchall() 
	cursor.close()
	# ---------------------------------------display earnings default 30 days ------------------------------------
	cursor = conn.cursor()
	query = "SELECT (sold_price * commission / 100) as profit FROM purchase natural join ticket where b_email = %s\
		and booking_agent_ID = %s"
	cursor.execute(query, (email,ID))
	data2= cursor.fetchall()
	cursor.close()
	tickets = 0
	earning = 0
	for each in data2:
		tickets += 1
		earning += each['profit']
	return render_template('home_booking_agent.html', email=email, flights=data1, commission=round(earning,2), tickets = tickets, avg_commission = round(earning/tickets,2))

#renders purchase ticket page for CUSTOMER --> queries all available flights from search bar on flights_customer.html
@app.route('/purchase_ticket_C', methods=["GET", "POST"])
def purchase_ticket_C():
	email = session['email']
	flight_num = request.form['flight_num']
	departure = request.form['departure_date_and_time']
	cursor = conn.cursor()
	query = "SELECT * FROM flight natural join reserve as f, ticket as t\
		 WHERE t.ticket_ID = f.ticket_ID and \
		 f.flight_num = %s and departure_date_and_time = %s \
		and card_type is NULL"
		#all available flights queried
	cursor.execute(query, (flight_num, departure))
	data = cursor.fetchall()
	cursor.close()
	return render_template('purchase_ticket_customer.html', flights = data, email=email)

#renders purchase ticket page for BOOKING AGENT --> queries all available flights from search bar on flights_booking_agent.html
@app.route('/purchase_ticket_BA', methods=["GET", "POST"])
def purchase_ticket_BA():
	email = session['email']
	flight_num = request.form['flight_num']
	departure = request.form['departure_date_and_time']
	cursor = conn.cursor()
	query = "SELECT * FROM flight natural join reserve as f, ticket as t\
		 WHERE t.ticket_ID = f.ticket_ID and \
		 f.flight_num = %s and departure_date_and_time = %s \
		and card_type is NULL"
		#all available flights queried
	cursor.execute(query, (flight_num, departure))
	data = cursor.fetchall()
	cursor.close()
	return render_template('purchase_ticket_booking_agent.html', flights = data, email=email)

#button BUY --> function renders template to get the payment information on the next page from CUSTOMER
@app.route('/confirming_purchase_C', methods=["GET", "POST"])
def confirming_purchase_C():
	email = session['email']
	ticket_ID = request.form['ticket_ID']
	sold_price = request.form['sold_price']
	return render_template("payment_customer.html", email=email, ticket_ID = ticket_ID, sold_price = sold_price)

#button BUY --> function renders tempalte to get the payment information on the next page from BOOKING AGENT 
@app.route('/confirming_purchase_BA', methods=["GET", "POST"])
def confirming_purchase_BA():
	email = session['email']
	ticket_ID = request.form['ticket_ID']
	sold_price = request.form['sold_price']
	return render_template("payment_booking_agent.html", email=email, ticket_ID = ticket_ID, sold_price = sold_price)


#-------CONFIRMS TICKET PURHCASE INSERTS INTO DATABASE PURCHASE INFO FOR CUSTOMER ----------------------------------------
@app.route('/payment_info_C', methods=["GET", "POST"])
def payment_info_C():
	# ticketID, sold_price, card_number, card_type, name, date
	# update ticket table with card information 
	# insert into purchase table 
	email = session['email']
	ticket_ID = request.form['ticket_ID']
	sold_price = request.form['sold_price'] #not used for queries, only used to display price to customer
	card_type = request.form['card_type']
	card_number = request.form['card_number']
	name = request.form['name']
	expiration_date = request.form['expiration_date']
	cursor = conn.cursor()
	query = "UPDATE ticket SET card_type = %s, card_number = %s, name = %s, expiration_date = %s, purhcase_date_and_time = (select NOW())\
		where ticket_ID = %s"
	cursor.execute(query, (card_type, card_number, name, expiration_date, ticket_ID))
	conn.commit()
	cursor.close()
	card_type = request.form['card_type']
	card_number = request.form['card_number']
	name = request.form['name']
	expiration_date = request.form['expiration_date']
	cursor = conn.cursor()
	query = "INSERT INTO purchase values(%s, %s, NULL, NULL, NULL, NULL)"
	cursor.execute(query, (ticket_ID, email))
	conn.commit()
	cursor.close()
	return redirect(url_for("confirmed_customer_purchase"))

#-------CONFIRMS TICKET PURHCASE INSERTS INTO DATABASE PURCHASE INFO FOR CUSTOMER ----------------------------------------
@app.route('/payment_info_BA', methods=["GET", "POST"])
def payment_info_BA():
	# ticketID, sold_price, card_number, card_type, name, date
	# update ticket table with card information 
	# insert into purchase table 
	email = session['email']
	ID = session['ID']
	c_email = request.form['c_email']
	ticket_ID = request.form['ticket_ID']
	sold_price = request.form['sold_price'] #not used for queries, only used to display price to customer
	card_type = request.form['card_type']
	card_number = request.form['card_number']
	name = request.form['name']
	expiration_date = request.form['expiration_date']
	cursor = conn.cursor()
	query = "UPDATE ticket SET card_type = %s, card_number = %s, name = %s, expiration_date = %s, purhcase_date_and_time = (select NOW())\
		where ticket_ID = %s"
	cursor.execute(query, (card_type, card_number, name, expiration_date, ticket_ID))
	conn.commit()
	cursor.close()
	card_type = request.form['card_type']
	card_number = request.form['card_number']
	name = request.form['name']
	expiration_date = request.form['expiration_date']
	cursor = conn.cursor()
	query = "INSERT INTO purchase values(%s, %s, %s, %s, %s)"  
	cursor.execute(query, (ticket_ID, c_email, email, ID, 10 ))   
	######################################################### TODO, CHANGE COMISSION RATE ##########################################################
	conn.commit()
	cursor.close()
	return redirect(url_for("confirmed_booking_agent_purchase"))

@app.route('/confirmed_customer_purchase')
def confirmed_customer_purchase():
	email = session['email']
	return render_template("confirmed_customer_purchase.html", email = email)

@app.route('/confirmed_booking_agent_purchase')
def confirmed_booking_agent_purchase():
	email = session['email']
	return render_template("confirmed_booking_agent_purchase.html", email = email)

#----------------------------custom range CUSTOMER bar graph of past purchases---------------------------------
#-------------queries all past purchase with customized date range and redirected to home CUSTOMER page--------
@app.route('/purchased_date_range_C', methods=['GET', 'POST'])
def purchased_date_range_C():
	email = session['email']
	begin = request.form['begin']
	end = request.form['end']
	cursor = conn.cursor()
	query = "SELECT sold_price as price, purhcase_date_and_time as date FROM ticket natural join customer\
		 WHERE email = %s and (%s >purhcase_date_and_time and purhcase_date_and_time > %s) "
	cursor.execute(query,(email, end, begin))
	data = cursor.fetchall()
	cursor.close()
	session['prices'] = ''
	session['dates'] = ''
	for result in data:
		session['prices'] += str(result['price']) + ' '
		session['dates'] += str(result['date']) + ','
	return redirect(url_for('home_customer'))
	
#search flights page for CUSTOMER
@app.route('/flights')
def flights():
	email = session['email']
	departure_searches = session['departure_searches']
	if 'return_searches' in session:
		return_searches = session['return_searches']
	else:
		return_searches = None
	return render_template('flights_customer.html', email=email, departure_searches=departure_searches,\
		return_searches = return_searches)

#search flights page for BOOKING AGENT
@app.route('/flights_booking_agent')
def flights_booking_agent():
	email = session['email']
	departure_searches = session['departure_searches']
	if 'return_searches' in session:
		return_searches = session['return_searches']
	else:
		return_searches = None
	return render_template('flights_booking_agent.html', email=email, departure_searches=departure_searches,\
		return_searches = return_searches)

@app.route('/flight_status')
def flight_status():
	email = session['email']
	statuses = session['statuses']
	return render_template('flight_status_customer.html', email=email, statuses=statuses)

@app.route('/flight_status_booking_agent')
def flight_status_booking_agent():
	email = session['email']
	statuses = session['statuses']
	return render_template('flight_status_booking_agent.html', email=email, statuses=statuses)

@app.route('/search_status_C', methods=['GET', 'POST'])
def search_status_C():
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

@app.route('/search_flights_C', methods=['GET', 'POST'])
def search_flights_C():
	email = session['email']
	departure = request.form['departure'].lower()
	arrival = request.form['arrival'].lower()
	departure_date = request.form['departure_date']
	return_date = request.form['return_date']
	cursor = conn.cursor();
	query = 'SELECT flight_num, departure_date_and_time FROM airport natural join arrival WHERE\
		 (name = %s or city = %s) and flight_num in \
			 (select flight_num FROM airport natural join departure where name = %s or city = %s)'
	cursor.execute(query, (arrival, arrival, departure, departure))
	data2 = cursor.fetchall()
	cursor.close()
	year = departure_date[0:4]
	month = departure_date[5:7]
	result = []
	for each in data2:
		if each['departure_date_and_time'].year == int(year) and each['departure_date_and_time'].month == int(month):
			result.append(each)
	session['departure_searches'] = result
	if return_date.strip() != '':
		print("HIIIII")
		print(return_date)
		print("HIIIII")
		cursor = conn.cursor();
		query = 'SELECT flight_num, departure_date_and_time FROM airport natural join arrival WHERE\
			(name = %s or city = %s) and flight_num in \
				(select flight_num FROM airport natural join departure where name = %s or city = %s)'
		cursor.execute(query, (departure, departure, arrival, arrival))
		data2 = cursor.fetchall()
		cursor.close()
		year = departure_date[0:4]
		month = departure_date[5:7]
		result = []
		for each in data2:
			if each['departure_date_and_time'].year == int(year) and each['departure_date_and_time'].month == int(month):
				result.append(each)
		session['return_searches'] = result
	return redirect(url_for('flights'))

#searching for flights for BA
@app.route('/search_flights_BA', methods=['GET', 'POST'])
def search_flights_BA():
	email = session['email']
	departure = request.form['departure'].lower()
	arrival = request.form['arrival'].lower()
	departure_date = request.form['departure_date']
	return_date = request.form['return_date']
	cursor = conn.cursor();
	query = 'SELECT flight_num, departure_date_and_time FROM airport natural join arrival WHERE\
		 (name = %s or city = %s) and flight_num in \
			 (select flight_num FROM airport natural join departure where name = %s or city = %s)'
	cursor.execute(query, (arrival, arrival, departure, departure))
	data2 = cursor.fetchall()
	cursor.close()
	year = departure_date[0:4]
	month = departure_date[5:7]
	result = []
	for each in data2:
		if each['departure_date_and_time'].year == int(year) and each['departure_date_and_time'].month == int(month):
			result.append(each)
	session['departure_searches'] = result
	if return_date.strip() != '':
		print("HIIIII")
		print(return_date)
		print("HIIIII")
		cursor = conn.cursor();
		query = 'SELECT flight_num, departure_date_and_time FROM airport natural join arrival WHERE\
			(name = %s or city = %s) and flight_num in \
				(select flight_num FROM airport natural join departure where name = %s or city = %s)'
		cursor.execute(query, (departure, departure, arrival, arrival))
		data2 = cursor.fetchall()
		cursor.close()
		year = departure_date[0:4]
		month = departure_date[5:7]
		result = []
		for each in data2:
			if each['departure_date_and_time'].year == int(year) and each['departure_date_and_time'].month == int(month):
				result.append(each)
		session['return_searches'] = result
	return redirect(url_for('flights_booking_agent'))
	
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
	session.clear()
	##logout all session variables TODO 
	return redirect('/')
	
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
