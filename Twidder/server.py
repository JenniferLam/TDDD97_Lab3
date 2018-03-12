from flask import app, request
from flask import Flask
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import database_helper
import json
import random

app = Flask(__name__, static_url_path = '')
app.debug = True

# Dictionary to store web socket and email
# One web socket for one user
# Email is the key
loggedUsers = {}
# Store the total number of online users
num_onlineuser = 0
# Store the total no. of views per user
view_table = {}

@app.before_request
def before_request():
   database_helper.connect_db()

@app.teardown_request
def teardown_request(exception):
   database_helper.close_db()

@app.route('/')
def root():
	return app.send_static_file('client.html')
	#return app.send_static_file('index.html')

@app.route('/websoc',methods=['GET'])
def webSocket():
    global num_onlineuser
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            # Receive the email and token from client side in json format
            message = ws.receive()
            if message is not None:
				print("[DEBUG] " + message)
				message = json.loads(message)
				msgtype = str(message['type'])
				email = str(message['email'])
				token = str(message['token'])

				# Sign in
				if msgtype == "signin":
					num_onlineuser += 1
					# Extract the ws if the user signed in before
					if email in loggedUsers:
						tmp_ws = loggedUsers[email]
					else:
						tmp_ws = ""

					# If the user did their second signin, 
					# then remove the token and redirect to welcome page in first sign in browser
					if tmp_ws != "":
						num_onlineuser -= 1 
						tmp_ws.send(json.dumps({"type":"autoSignOut", "value":"SignOut"}))

					# Store the latest ws in the dict
					loggedUsers[email] = ws
					if not email in view_table:
						view_table[email] = 0
				
				# Refresh the page
				elif msgtype == "reload":
					num_onlineuser += 1
					loggedUsers[email] = ws

				# Close the browser
				elif msgtype == "unload":
					num_onlineuser -= 1
					loggedUsers[email] = ""
					
				# Sign out
				elif msgtype == "signout":
					loggedUsers[email] = ""
					num_onlineuser -= 1

				# Update the total number of posts
				elif msgtype == "postMsg":
					num = database_helper.get_num_post(email)
					if email in loggedUsers and loggedUsers[email] != "":
						totalPosts = database_helper.get_totalnum_post()
						loggedUsers[email].send(json.dumps({"type":"postMsg", "value":str(num), "total":str(totalPosts)}))
				
				# Update the total number of views per user
				elif msgtype == "updateuserview":
					value = str(message['value'])
					if value == "search":
						previousEmail = str(message['previousEmail'])
						if email in view_table:
							view_table[email] += 1
						else:
							view_table[email] = 1

						print (previousEmail)
						if previousEmail != "null":
							view_table[previousEmail] = view_table[previousEmail] - 1
							
					elif value == "signout":
						view_table[email] -= 1

					totalUsers = database_helper.get_num_user()
					if email in loggedUsers and loggedUsers[email] != "":
						loggedUsers[email].send(json.dumps({"type":"updateUserView", "value":str(view_table[email]), "total":str(totalUsers)}))

					if previousEmail in loggedUsers and loggedUsers[previousEmail] != "":
						loggedUsers[previousEmail].send(json.dumps({"type":"updateUserView", "value":str(view_table[previousEmail]), "total":str(totalUsers)}))

				# Update the total number of online users	
				if msgtype != "postmsg":
					for l in loggedUsers:
						tmp_ws = loggedUsers[l]
						if  tmp_ws != "":
							totalUsers = database_helper.get_num_user()
							tmp_ws.send(json.dumps({"type":"updateUserCnt", "value":str(num_onlineuser), "total":str(totalUsers)}))
							tmp_ws.send(json.dumps({"type":"updateUserView", "value":str(view_table[l]), "total":str(totalUsers)}))
            else:
                print("[Debug] Exit loop")
                loggedUsers[email] = ""
                break
	return ""

@app.route('/signin', methods=['POST'])
def sign_in():
	
	try:
		email = request.json['email']
		password = request.json['password']
	except:
		return json.dumps({"success": False, "message":"Json key error."}),400
	
	db_password = database_helper.get_UserPW(email)
	if password != db_password:
		return json.dumps({"success": False, "message":"Wrong username or password."}),404
	
	tmp_token = database_helper.get_tokenByEmail(email)
	if tmp_token:
		database_helper.delete_token(tmp_token[0])
		#return json.dumps({"success": False, "message":"User already signed in."}),501
	
	token = ""
	letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"  
	for i in range(0,36):
		index = random.randint(0,len(letters)-1)
		token += letters[index]
	
	database_helper.add_token(email, token)
	return json.dumps({"success": True, "message":"Successfully signed in.", "data": token}),200
		

@app.route('/signup', methods=['POST'])
def sign_up():
	try: 
		email = request.json['email']
		password = request.json['password']
		firstname = request.json['firstname']
		familyname = request.json['familyname']
		gender = request.json['gender']
		city = request.json['city']
		country = request.json['country']
	except:
		return json.dumps({"success": False, "message":"Json key error."}),400

	# Mandatory field and data type checking
	if (email == "" or password == "" or firstname =="" or familyname == "" or gender == "" or city == "" or country == "" or len(password) < 8):
		return json.dumps({"success": False, "message":"Form data missing or incorrect type."}),403

	# Check if the user exists in the userprofile table
	if database_helper.find_user(email):
		return json.dumps({"success": False, "message":"User already exists."}),501

	database_helper.add_user(email, password, firstname, familyname, gender, city, country)
	return json.dumps({"success": True, "message":"Successfully created a new user."}),200

@app.route('/signout', methods=['POST'])
def sign_out():
	try:
		token = request.json['token']
	except:
		return json.dumps({"success": False, "message":"Json key error."}),400

	is_there = database_helper.get_emailByToken(token)
	
	if not is_there:
		return json.dumps({"success": False, "message":"You are not signed in"}),403

	database_helper.delete_token(token)


	return json.dumps({"success": True, "message":"Successfully signed out"}),200

@app.route('/getUserDataByToken/<token>', methods=['GET'])
def get_user_data_by_token(token = None):
	
	if token is None:
		return json.dumps({"success": False, "message":"Key error."}),400

	# Check if the token exists
	if not token:
		return json.dumps({"success": False, "message":"You are not signed in."}),403

	# Check if the current user exists
	email = database_helper.get_emailByToken(token)
	if not email:
		return json.dumps({"success": False, "message":"No such user."}),404
	
	# Return the user profile
	data = database_helper.find_user(email)
	numOfPost = database_helper.get_num_post(email)
	totalOfPost = database_helper.get_totalnum_post()
	return json.dumps({"success": True, "message": "User data retrieved.", "data": [dict(x) for x in data], "NumOfPost":str(numOfPost), "TotalOfPost":str(totalOfPost)}),200

@app.route('/getUserDataByEmail/<token>/', defaults={'email':""}, methods=['GET'])	
@app.route('/getUserDataByEmail/<token>/<email>', methods=['GET'])
def get_user_data_by_email(token = None, email=None):
	if token is None or email is None:
		return json.dumps({"success": False, "message":"Key error."}),400

	# Check if the token exists (current user)
	if not token:
		return json.dumps({"success": False, "message":"You are not signed in."}),403

	# Check if the current user exists
	currentUser = database_helper.get_emailByToken(token)
	if not currentUser:
		return json.dumps({"success": False, "message":"No such user."}),404
	
	# Return the user profile
	data = database_helper.find_user(email)
	if data:
		return json.dumps({"success": True, "message": "User data retrieved.", "data": [dict(x) for x in data]}),200
	# Check if the target user exists
	else:
		return json.dumps({"success": False, "message":"No such user."}),404

@app.route('/postMsg', methods=['POST'])
def post_message():
	try:
		token = request.json['token']
		toEmail = request.json['toEmail']
		content = request.json['content']
	except:
		return json.dumps({"success": False, "message":"Json key error."}),400

	# Check if the user signs in or not
	fromEmail = database_helper.get_emailByToken(token)
	if not fromEmail:
		return json.dumps({"success": False, "message":"You are not signed in."}),403
		
	# Check if the users exists or not
	if not database_helper.find_user(toEmail):
		return json.dumps({"success": False, "message":"No such user."}),404		

	database_helper.post_msg(toEmail, fromEmail, content)	
	return json.dumps({"success": True, "message":"Message posted."}),200

@app.route('/getUserMessagesByToken/<token>', methods=['GET'])
def get_user_messages_by_token(token = None):

	if token is None:
		return json.dumps({"success": False, "message":"Key error."}),400
	
	# Check if the token exists
	if not token:
		return json.dumps({"success": False, "message":"You are not signed in."}),403

	# Check if the current user exists
	email = database_helper.get_emailByToken(token)
	if not email:
		return json.dumps({"success": False, "message":"No such user."}),404
	
	# Return all messages of current user
	message = database_helper.get_msglist(email)
	return json.dumps({"success": True, "message": "User data retrieved.", "data": [dict(x) for x in message]}),200

@app.route('/getUserMessagesByEmail/<token>/<toEmail>', methods=['GET'])
def get_user_messages_by_email(token = None, toEmail = None):
	
	if token is None or toEmail is None:
		return json.dumps({"success": False, "message":"Key error."}),400

	# Check if the token exists (current user)
	if not token:
		return json.dumps({"success": False, "message":"You are not signed in."}),403

	# Check if the current user exists
	email = database_helper.get_emailByToken(token)
	if not email:
		return json.dumps({"success": False, "message":"No such user."}),404
	
	# Check if the target user exists
	if not database_helper.find_user(toEmail):
		return json.dumps({"success": False, "message":"No such user."}),404
		
	# Return all messages of target user
	message = database_helper.get_msglist(toEmail)
	return json.dumps({"success": True, "message": "User data retrieved.", "data": [dict(x) for x in message]}),200
		

@app.route('/changePassword', methods=['POST'])
def change_password():
	try:
		token = request.json['token']
		oldPassword = request.json['oldPassword']
		newPassword = request.json['newPassword']
	except:
		return json.dumps({"success": False, "message":"Json key error."}),400

	# Check if the user signs in 
	# Check if the token is valid
	email = database_helper.get_emailByToken(token)
	if not email:
		return json.dumps({"success": False, "message":"You are not signed in."}),403

	# Check if the old password is correct
	# If yes, change password
	if (oldPassword == database_helper.get_UserPW(email)):
		if len(newPassword)<8:
			return json.dumps({"success": False, "message":"Password should have at least 8 characters."}),403
		
		if (oldPassword == newPassword):
			return json.dumps({"success": False, "message":"New password cannot be as same as old password."}),403
		
		database_helper.change_PW(email,newPassword)
		return json.dumps({"success": True, "message":"Password changed."}),200
	
	else:
		return json.dumps({"success": False, "message":"Wrong password."}),403

if __name__ == "__main__":
	http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
	http_server.serve_forever()
	
