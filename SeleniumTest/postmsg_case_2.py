from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import common

# Create chrome webdriver
driver=webdriver.Chrome()

# Test Case Information
result = True
step_num = 1
f = common.createFileObj('postMsg_case_2')
scenario = 'Scenario: Post a message in browse tab'
precondition = 'Pre-condition: The user signed in'
common.printTitle(f, scenario, precondition)

# Go to Twidder
driver.get("http://127.0.0.1:5000")
f.write(str(step_num)+'. '+'Open the browser\n')
step_num+= 1

# Fill in the username and password
username = driver.find_element_by_id("signin_email")
password = driver.find_element_by_id("signin_pw")

username.send_keys("abc@abc")
f.write(str(step_num)+'. '+'Fill in the username\n')
step_num+= 1

password.send_keys("abcd1234")
f.write(str(step_num)+'. '+'Fill in the password\n')
step_num+= 1

# Submit the login form
signin_button = driver.find_element_by_id("btn_signin")
signin_button.click()
f.write(str(step_num)+'. '+'Click the Sign In button\n')
step_num+= 1

# Check if the sign in is success
# Wait until the username is displayed
element_present = EC.presence_of_element_located((By.NAME,'home_personalInfo_email'))
WebDriverWait(driver, 90).until(element_present)
f.write(str(step_num)+'. '+'Go to the profile view\n')
step_num+= 1

driver.save_screenshot('./result/postmsg_case_2_1.png')
	
# To make sure if the user is as same as sign in username
email = driver.find_element_by_name("home_personalInfo_email")
f.write(str(step_num)+'. '+'Verify the username ')
step_num+= 1

if email.text != "abc@abc":
	result = False
	f.write('(WRONG USER): '+ email.text)
f.write('\n')

# Go to browse tab
browse_tab = driver.find_element_by_id("tab_browse")
browse_tab.click()
f.write(str(step_num)+'. '+'Go to Browse Tab\n')
step_num+= 1

# Search a friend
searchBar = driver.find_element_by_name("searchEmail")
target_user = "def@def"
searchBar.send_keys(target_user)
f.write(str(step_num)+'. '+'Type a friend\'s email\n')
step_num+= 1

search_button = driver.find_element_by_id("searchBtn")
search_button.click()
f.write(str(step_num)+'. '+'Click the Search Button\n')
step_num+= 1

# Display the user's profile
element_present = EC.presence_of_element_located((By.NAME,'email_otherUser'))
WebDriverWait(driver, 90).until(element_present)
email_browse = driver.find_element_by_name("email_otherUser")
f.write(str(step_num)+'. '+'The user profile is displayed ')
step_num+= 1
if email_browse.text != target_user:
	result = False
	f.write("(WRONG USER): "+email_browse.text)
f.write('\n')

# Post message to own profile
postbox = driver.find_element_by_id("postBox_browse")
post_button = driver.find_element_by_id("btn_post_browse")

content = "Testing on 10 Mar 2018 from abc@abc"
postbox.send_keys(content)
f.write(str(step_num)+'. '+'Write the message in the post area\n')
step_num+= 1

post_button.click()

driver.save_screenshot('./result/postmsg_case_2_2.png')
# Feedback is expected from the server
feedback = driver.find_element_by_id("errormsgPostWall_browse")
msgtext = "Message posted."
f.write(str(step_num)+'. '+'Receive the feedback from the server - '+msgtext)
step_num+= 1

if feedback.text != msgtext:
	result = False
	f.write('(UNEXPECTED FEEDBACK): '+ feedback.text)
f.write('\n')

# The latest message is displayed on the wall automatically
writer = driver.find_element_by_xpath("//*[@id=\"msgWall_browse\"]/div[1]")
postedMsg = driver.find_element_by_xpath("//*[@id=\"msgWall_browse\"]/div[2]")

driver.save_screenshot('./result/postmsg_case_2_3.png')

f.write(str(step_num)+'. '+'The latest message is displayed on the wall ')
step_num+= 1
if writer.text!= "From: abc@abc" or postedMsg.text != content:
	result = False
	f.write('(MESSAGE IS OUTDATED)')
f.write('\n')
f.write(writer.text + '\n')
f.write(postedMsg.text + '\n')

# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()
