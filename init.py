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
		cursor = conn.cursor()
		query = 'SELECT name FROM works WHERE username = %s'
		cursor.execute(query,(username))
		airline_name = cursor.fetchone()
		session['name'] = airline_name['name']
		cursor.close()
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
	name = request.form['name']

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
		cursor = conn.cursor()
		ins = "INSERT INTO works VALUES(%s, %s)"
		cursor.execute(ins, (username, name))
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
			WHERE email = %s and (year(CURRENT_TIMESTAMP) - year(purhcase_date_and_time)) * 12 + \
					(month(CURRENT_TIMESTAMP) - month(purhcase_date_and_time)) <= 12" #fix mispelling in db
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
		FROM purchase natural join reserve natural join flight WHERE b_email = %s and booking_agent_ID = %s'
	cursor.execute(query, (email, ID))
	data1 = cursor.fetchall() 
	cursor.close()
	tickets = 0 
	earning = 0 
	# -------------------------------------display earnings default 30 days ------------------------------------
	if 'custom_earnings' not in session:
		cursor = conn.cursor()
		query = "SELECT (sold_price * commission / 100) as profit FROM purchase natural join ticket where b_email = %s\
			and booking_agent_ID = %s and \
				((year(CURRENT_TIMESTAMP) - year(purhcase_date_and_time)) * 365 + \
					(month(CURRENT_TIMESTAMP) - month(purhcase_date_and_time)) * 30  + \
						day(CURRENT_TIMESTAMP) - day(purhcase_date_and_time)) <= 30"
		cursor.execute(query, (email,ID))
		prices= cursor.fetchall()
		cursor.close()
		for each in prices:
			tickets += 1
			earning += each['profit']
	#--------------------------------------display custom default 30 day earnings -----------------------------
	else: #with custom range
		prices = session['custom_earnings'].strip().split(' ')
		for each in prices:
			tickets += 1
			earning += float(each)
			print(each)
	avg_commission = round(earning/tickets,2) if tickets != 0 else 0
	#-----------------------------------------bar graph for TOP FIVE CUSTOMERS--------------------------------
	customers1 = [] #five top customer emails
	ticket_count = [] 
	colors = []
	cursor = conn.cursor()
	query = "SELECT count(ticket_ID) as tickets, c_email FROM ticket natural join purchase\
			WHERE b_email = %s and booking_agent_ID = %s and \
				 ((year(CURRENT_TIMESTAMP) - year(purhcase_date_and_time)) * 12 + \
					(month(CURRENT_TIMESTAMP) - month(purhcase_date_and_time))) <= 6 \
						GROUP BY c_email ORDER BY tickets DESC LIMIT 5" 
	cursor.execute(query, (email, ID))
	data= cursor.fetchall()
	cursor.close()
	for each in data:
		customers1.append(each['c_email'])
		ticket_count.append(each['tickets'])

	#-----------------------------------------bar graph for TOP FIVE COMMISSION--------------------------------------
	customers2 = [] #five top customer emails
	commissions = [] 
	colors = []
	cursor = conn.cursor()
	query = "SELECT sum(sold_price * commission / 100) as profit, c_email FROM ticket natural join purchase\
			WHERE b_email = %s and booking_agent_ID = %s and \
				 ((year(CURRENT_TIMESTAMP) - year(purhcase_date_and_time)) * 12 + \
					(month(CURRENT_TIMESTAMP) - month(purhcase_date_and_time))) <= 12 \
						GROUP BY c_email ORDER BY profit DESC LIMIT 5"
	cursor.execute(query, (email, ID))
	data= cursor.fetchall()
	cursor.close()
	for each in data:
		customers2.append(each['c_email'])
		commissions.append(round(each['profit'],2))
		print(each)
	return render_template('home_booking_agent.html', email=email, flights=data1, commission=round(earning,2), \
		tickets = tickets, max1 = 5, avg_commission = avg_commission, ticket_count = ticket_count, customers1 = customers1,\
			customers2 = customers2, commissions = commissions, max2 = 1000)

#home page for airline staff
@app.route('/home_airline_staff')
def home_airline_staff():
	username = session['username']
	name = session['name']
	# ---------------------------------------display purchased tickets-------------------------------
	cursor = conn.cursor()
	query = 'SELECT name, flight_num, departure_date_and_time, arrival_date_and_time, status \
		FROM purchase natural join reserve natural join flight WHERE c_email = %s and \
			departure_date_and_time - (select now()) > 0'
	cursor.execute(query, (username))
	data1 = cursor.fetchall()
	cursor.close()
	# ---------------------------------------display past flights and comments ------------------------
	cursor = conn.cursor()
	query = 'SELECT name, flight_num, departure_date_and_time, arrival_date_and_time, status \
		FROM purchase natural join reserve natural join flight WHERE c_email = %s and \
			arrival_date_and_time - (select now()) <= 0'
	cursor.execute(query, (username))
	data2 = cursor.fetchall()
	cursor.close()
	#-------------------------------all booking agents------------------------------------------------
	cursor = conn.cursor()
	query = "Select email from booking_agent WHERE email is not NULL"
	cursor.execute(query)
	booking_agents1 = cursor.fetchall()
	cursor.close()
	#-----------------------------top five booking agents tickets past month---------------------------
	cursor = conn.cursor()
	query = "SELECT count(ticket_ID) as tickets, b_email, booking_agent_ID FROM ticket natural join purchase\
				WHERE (b_email is not NULL) and \
					((year(CURRENT_TIMESTAMP) - year(purhcase_date_and_time)) * 12 + \
					(month(CURRENT_TIMESTAMP) - month(purhcase_date_and_time))) <= 1 \
						GROUP BY b_email, booking_agent_ID ORDER BY tickets DESC"
	cursor.execute(query)
	booking_agents2 = cursor.fetchall()
	cursor.close()
	#--------------------------top five booking agents tickets past year--------------------------------
	cursor = conn.cursor()
	query = "SELECT count(ticket_ID) as tickets, b_email, booking_agent_ID FROM ticket natural join purchase\
			WHERE (b_email is not NULL) and \
				((year(CURRENT_TIMESTAMP) - year(purhcase_date_and_time)) * 12 + \
					(month(CURRENT_TIMESTAMP) - month(purhcase_date_and_time))) <= 12 \
						GROUP BY b_email, booking_agent_ID ORDER BY tickets DESC"
	cursor.execute(query)
	booking_agents3 = cursor.fetchall()
	cursor.close()
	#------------------------------top five booking agents commissions past year ----------------------------
	cursor = conn.cursor()
	query = "SELECT sum(sold_price * commission / 100) as profit, b_email, booking_agent_ID FROM ticket natural join purchase\
			WHERE (b_email is not NULL) and \
				((year(CURRENT_TIMESTAMP) - year(purhcase_date_and_time)) * 12 + \
					(month(CURRENT_TIMESTAMP) - month(purhcase_date_and_time))) <= 12 \
						GROUP BY b_email, booking_agent_ID ORDER BY profit DESC"
	cursor.execute(query)
	booking_agents4 = cursor.fetchall()
	cursor.close()
	for each in booking_agents4:
		each['profit'] = round(each['profit'], 2)
	#---------------------------------most freq customer-------------------------------------------------------
	cursor = conn.cursor()
	query = "Select c_email from flight as f , reserve as r , ticket as t, purchase as p where \
		f.flight_num = r.flight_num and f.name = %s and  r.ticket_ID = t.ticket_ID \
			and t.ticket_ID = p.ticket_ID group by c_email order by count(t.ticket_ID) desc LIMIT 1"
	cursor.execute(query, (name))
	freq_customer = cursor.fetchone()
	cursor.close()

	return render_template('home_airline_staff.html', username = username, name=name, freq_customer = freq_customer,\
		booking_agents1 = booking_agents1, booking_agents2=booking_agents2, booking_agents3=booking_agents3, booking_agents4=booking_agents4)

#searches up a particular customer's flights of specific airline of AIRLINE STAFF'S
@app.route("/search_customer_purchases", methods=['GET', 'POST'])
def search_customer_purchases():
	name = session['name']
	c_email = request.form['c_email']
	cursor = conn.cursor()
	query = "Select f.flight_num from flight as f , reserve as r , ticket as t, purchase as p\
			where f.flight_num = r.flight_num and f.name = %s and r.ticket_ID = t.ticket_ID and \
 				t.ticket_ID = p.ticket_ID and p.c_email = %s"
	cursor.execute(query, (name, c_email))
	data = cursor.fetchall()
	cursor.close()
	session['customer_purchases'] = data
	session['c_email'] = c_email
	return redirect(url_for('search_customers'))

#render tempplate for customer and their past flights with specific airline of AIRLINE STAFF's
@app.route("/search_customers")
def search_customers():
	name = session['name']
	customer_purchases = session['customer_purchases']
	c_email = session['c_email']
	return render_template('search_customer_purchases.html', name = name, customer_purchases = customer_purchases, c_email = c_email)

#----------------------------custom range BOOKING AGENT bar graph of past purchases---------------------------------
#-------------queries all past purchase with customized date range and redirected to home CUSTOMER page--------
@app.route('/earnings_date_range_BA', methods=['GET', 'POST'])
def earnings_date_range_BA():
	email = session['email']
	ID = session['ID']
	begin = request.form['begin']
	end = request.form['end']
	cursor = conn.cursor()
	query = "SELECT sold_price as price FROM ticket natural join purchase\
		 WHERE b_email = %s and booking_agent_ID = %s and (%s >purhcase_date_and_time and purhcase_date_and_time > %s) "
	cursor.execute(query,(email, ID, end, begin))
	data = cursor.fetchall()
	cursor.close()
	session['custom_earnings'] = ''
	for result in data:
		session['custom_earnings'] += str(result['price']) + ' '
	return redirect(url_for('home_booking_agent'))

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

#search flights page for AIRLINE STAFF
@app.route('/flights_airline_staff')
def flights_airline_staff():
	username = session['username']
	departure_searches = session['departure_searches']
	if 'return_searches' in session:
		return_searches = session['return_searches']
	else:
		return_searches = None
	return render_template('flights_airline_staff.html', username=username, departure_searches=departure_searches,\
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
	return render_template('flight_status_booking_agent.html', username=username, statuses=statuses)

@app.route('/flight_status_airline_staff') 
def flight_status_airline_staff():
	username = session['username']
	statuses = session['statuses']
	return render_template('flight_status_airline_staff.html', username=username, statuses=statuses)

@app.route('/search_status_C', methods=['GET', 'POST'])
def search_status_C():
	email = session['email']
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']
	cursor = conn.cursor()
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
	airline_name = request.form['airline_name']
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

@app.route('/search_status_AS', methods=['GET', 'POST'])
def search_status_AS():
	username = session['username']
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']
	cursor = conn.cursor()
	query = 'SELECT name, flight_num, status, departure_date_and_time FROM flight WHERE\
		 name = %s and flight_num = %s and departure_date_and_time = %s \
		 	 and arrival_date_and_time = %s'
	cursor.execute(query, (airline_name, flight_num, departure_date, arrival_date))
	data3 = cursor.fetchall()
	cursor.close()
	session['statuses'] = data3
	return redirect(url_for('flight_status_airline_staff'))

#updates status of flight for AIRLINE STAFF
@app.route('/update_flight_status_AS', methods=["GET", "POST"])
def update_flight_status_AS():
	flight_num = request.form['flight_num']
	departure_time = request.form['departure_date_and_time']
	name = request.form['name']
	status = request.form['status']
	cursor = conn.cursor()
	query = "UPDATE flight SET status = %s WHERE flight_num = %s and departure_date_and_time = %s and name = %s"
	cursor.execute(query, (status, flight_num, departure_time,name))
	conn.commit()
	cursor.close()
	return redirect(url_for('home_airline_staff'))

#create new flight page for AIRLINE STAFF
@app.route('/create_flight_page')
def create_flight_page():
	name = session['name']
	username = session['username']
	return render_template('create_flight_airline_staff.html', username=username, name=name)

#creates new flight for AIRLINE STAFF
@app.route('/create_flight_AS', methods=['GET','POST'])
def create_flight_AS():
	name = session['name']
	flight_num = request.form['flight_num']
	departure_date_and_time=request.form['departure_date_and_time']
	arrival_date_and_time=request.form['arrival_date_and_time']
	base_price=request.form['base_price']
	status=request.form['status']
	departure = request.form['departure']
	arrival = request.form['arrival']
	ID_num = request.form['ID_num']
	#--------------------------------------------INSERT INTO FLIGHT-------------------------------------------------
	cursor = conn.cursor()
	query = "insert into flight values(%s, %s, %s, %s, %s, %s)"
	cursor.execute(query, (flight_num, departure_date_and_time, name, arrival_date_and_time, base_price, status))
	conn.commit()
	cursor.close()
	#------------------------------------------INSERT INTO ARRIVAL------------------------------------------------
	cursor = conn.cursor() 
	query = "insert into arrival values(%s, %s, %s)"
	print(arrival)
	cursor.execute(query, (flight_num, departure_date_and_time, arrival))
	conn.commit()
	cursor.close()
	#------------------------------------------INSERT INTO DEPARTURE------------------------------------------------
	cursor = conn.cursor() 
	query = "insert into departure values(%s, %s, %s)"
	cursor.execute(query, (flight_num, departure_date_and_time, departure))
	conn.commit()
	cursor.close()
	#------------------------------------------INSERT INTO HAS ----------------------------------------------------
	cursor = conn.cursor() 
	query = "insert into has values(%s, %s, %s)"
	cursor.execute(query, (flight_num, departure_date_and_time, ID_num))
	conn.commit()
	cursor.close()
	return redirect(url_for('home_airline_staff'))

#create new airport page for AIRLINE STAFF
@app.route('/create_airport_page')
def create_airport_page():
	return render_template('create_airport_airline_staff.html')

#create new airport for AIRLINE STAFF
@app.route('/create_airport_AS', methods=['GET','POST'])
def create_airport_AS():
	name = request.form['name']
	city = request.form['city']
	cursor = conn.cursor() 
	ins = "insert into airport values(%s, %s)"
	cursor.execute(ins, (name, city))
	conn.commit()
	cursor.close()
	return redirect(url_for('home_airline_staff'))

#create new airplane page for AIRLINE STAFF
@app.route('/create_airplane_page')
def create_airplane_page():
	name = session['name']
	username = session['username']
	return render_template('create_airplane_airline_staff.html', username=username, name=name)

#creates new airplane for AIRLINE STAFF
@app.route ('/create_airplane_AS', methods=['GET','POST'])
def create_airplane_AS():
	name = session['name']
	ID_num = request.form['ID_num']
	seats = request.form['num_of_seats']
	cursor = conn.cursor()
	ins = "insert into airplane values(%s, %s)"
	cursor.execute(ins, (ID_num, seats))
	conn.commit()
	cursor.close()
	cursor = conn.cursor()
	ins = "insert into owns values(%s, %s)"
	cursor.execute(ins, (name, ID_num))
	conn.commit()
	cursor.close()
	return redirect(url_for('confirmation_page_airplane'))

#displays all airplanes of airline that AIRLINE STAFF works for 
@app.route('/confirmation_page_airplane')
def confirmation_page_airplane():
	username = session['username']
	name = session['name']
	cursor = conn.cursor()
	query = "Select ID_num from owns natural join works where username = %s"
	cursor.execute(query, (username))
	data = cursor.fetchall()
	cursor.close()
	return render_template('confirmation_page_airplane.html', airplanes = data, name = name)

#searching for fights for CUSTOMER
@app.route('/search_flights_C', methods=['GET', 'POST'])
def search_flights_C():
	email = session['email']
	departure = request.form['departure']
	arrival = request.form['arrival']
	departure_date = request.form['departure_date']
	return_date = request.form['return_date']
	cursor = conn.cursor()
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

#searching for flights for BOOKING AGENT
@app.route('/search_flights_BA', methods=['GET', 'POST'])
def search_flights_BA():
	email = session['email']
	departure = request.form['departure']
	arrival = request.form['arrival']
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

#searching for flights for AIRLINE STAFF
@app.route('/search_flights_AS', methods=['GET', 'POST'])
def search_flights_AS():
	username = session['username']
	departure = request.form['departure']
	arrival = request.form['arrival']
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
	return redirect(url_for('flights_airline_staff'))

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
