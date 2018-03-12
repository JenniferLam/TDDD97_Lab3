import sqlite3
from flask import g

DATABASE = 'database.db'

def connect_db():
  g.db = sqlite3.connect(DATABASE)
  g.db.row_factory = sqlite3.Row
  g.db.text_factory = str

def close_db():
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

# Add a token to login table
# Will be used in sign in
def add_token(email, token):
  
  cur = g.db.execute("insert into login values (?,?)",[email,token])
  g.db.commit()

# Remove the token for sign out   
def delete_token(token):
   cur = g.db.execute("delete from login where token = ?",[token]) 
   g.db.commit()

# Get user password in userprofile table
# Will be used in sign in, change password
def get_UserPW(email):
  
  cur = g.db.execute("select password from userprofile where email = ?", [email])
  result = cur.fetchone()
  cur.close()

  if result:
    password = result[0]
  else:
    password = ""

  return password

# Create a new user profile
def add_user(email, password, firstname, familyname, gender, city, country):
  cur = g.db.execute('''insert into userprofile 
  values (?,?,?,?,?,?,?)''',[email,firstname,familyname,gender,city,country,password])
  g.db.commit()

# Check if the user exists in the userprofile table
# If yes, return all user information
def find_user(email):
  cur = g.db.execute('''select  email, firstname,familyname,gender,city,country
    from userprofile where email = ?''', [email])
  result = cur.fetchall()
  cur.close()
  return result

# Return the token from the login table
def get_tokenByEmail(email):
  cur = g.db.execute("select token from login where email = ?", [email])
  token = cur.fetchone()
  cur.close()

  return token

# Return the email searching by token from login table
def get_emailByToken(token):
  cur = g.db.execute("select email from login where token = ?", [token])
  result = cur.fetchone()
  if result:
    email = result[0]
  else:
    email = ""
  return email

# Post message to user
def post_msg(toEmail, fromEmail, content):
  cur = g.db.execute("insert into message values (?,?,?)",[toEmail, fromEmail,content])
  g.db.commit()  

# Return all messages of a user
def get_msglist(toEmail):
  cur = g.db.execute("select * from message where toemail = ?", [toEmail])
  result = cur.fetchall()
  cur.close()

  if result:
    return result
  else:
    return ""

def change_PW(email, newPassword):
  cur = g.db.execute('''
    UPDATE userprofile
    SET password = ?
    WHERE email = ?
    ''',[newPassword,email])
  g.db.commit()


def get_num_post(email):
  cur = g.db.execute("select count(*) from message where toemail = ?", [email])
  result = cur.fetchone()
  cur.close()
  return result[0]

def get_num_onlineuser():
  cur = g.db.execute("select count(*) from login")
  result = cur.fetchone()
  cur.close()
  return result[0]

def get_num_user():
  cur = g.db.execute("select count(*) from userprofile")
  result = cur.fetchone()
  cur.close()
  return result[0]



