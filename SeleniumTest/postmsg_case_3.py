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
f = common.createFileObj('postMsg_case_3')
scenario = 'Scenario: Post a message to same user and the message can be retrieved in home and browse tab'
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

driver.save_screenshot('./result/postmsg_case_3_1.png')
	
# To make sure if the user is as same as sign in username
email = driver.find_element_by_name("home_personalInfo_email")
f.write(str(step_num)+'. '+'Verify the username ')
f.write(common.compareText("abc@abc",email.text,"username"))
step_num+= 1

# Post message to own profile
postbox_home = driver.find_element_by_name("postArea")
post_button_home = driver.find_element_by_id("btn_post_home")

content = "This message should be displayed in home and browse tab"
postbox_home.send_keys(content)
f.write(str(step_num)+'. '+'Write the message in the post area in Home Tab\n')
step_num+= 1

post_button_home.click()

# Feedback is expected from the server
feedback_home = driver.find_element_by_id("errormsgPostWall_home")
msgtext = "Message posted."
f.write(str(step_num)+'. '+'Receive the feedback from the server - '+msgtext+"\n")
f.write(common.compareText(msgtext,feedback_home.text,"feedback"))
step_num+= 1

driver.save_screenshot('./result/postmsg_case_3_2.png')

# The latest message is displayed on the wall automatically
writer_home = driver.find_element_by_xpath("//*[@id=\"msgWall\"]/div[2]/div/div[1]/div")
postedMsg_home = driver.find_element_by_xpath("//*[@id=\"msgWall\"]/div[2]/div/div[2]/div[1]/div")

driver.save_screenshot('./result/postmsg_case_3_3.png')

f.write(str(step_num)+'. '+'The latest message is displayed on the wall \n')
step_num+= 1
f.write(common.compareText("From: abc@abc",writer_home.text,"writer"))
f.write(common.compareText(content,postedMsg_home.text,"post message"))

# Go to browse tab
browse_tab = driver.find_element_by_id("tab_browse")
browse_tab.click()
f.write(str(step_num)+'. '+'Go to Browse Tab\n')
step_num+= 1

# Search own user profile
searchBar = driver.find_element_by_name("searchEmail")
target_user = "abc@abc"
searchBar.send_keys(target_user)
f.write(str(step_num)+'. '+'Search for the current user profile\'s email\n')
step_num+= 1

search_button = driver.find_element_by_id("searchBtn")
search_button.click()
f.write(str(step_num)+'. '+'Click the Search Button\n')
step_num+= 1

# Display the user's profile
element_present = EC.presence_of_element_located((By.ID,'email_otherUser'))
WebDriverWait(driver, 90).until(element_present)
email_browse = driver.find_element_by_id("email_otherUser")

driver.save_screenshot('./result/postmsg_case_3_4.png')

f.write(str(step_num)+'. '+'The user profile is displayed \n')
f.write(common.compareText(target_user,email_browse.text,"username"))
step_num+= 1

# The message posted in home tab should be retrieved
writer_browse = driver.find_element_by_xpath("//*[@id=\"msgWall_browse\"]/div[2]/div/div[1]/div")
postedMsg_browse = driver.find_element_by_xpath("//*[@id=\"msgWall_browse\"]/div[2]/div/div[2]/div[1]/div")

driver.save_screenshot('./result/postmsg_case_3_5.png')

f.write(str(step_num)+'. '+'The message posted in home tab is retrieved in browse tab \n')
f.write(common.compareText("From: abc@abc",writer_browse.text,"writer"))
f.write(common.compareText(content,postedMsg_browse.text,"post message"))
step_num+= 1

# Post message to own profile
postbox_browse = driver.find_element_by_id("postBox_browse")
post_button_browse = driver.find_element_by_id("btn_post_browse")

content = "Testing on 10 Mar 2018 from abc@abc"
postbox_browse.send_keys(content)
f.write(str(step_num)+'. '+'Write the message in the post area\n')
step_num+= 1

post_button_browse.click()

driver.save_screenshot('./result/postmsg_case_3_6.png')

# Feedback is expected from the server
feedback_browse = driver.find_element_by_id("errormsgPostWall_browse")
msgtext = "Message posted."
f.write(str(step_num)+'. '+'Receive the feedback from the server - '+msgtext+"\n")
f.write(common.compareText(msgtext,feedback_browse.text,"feedback"))
step_num+= 1

# The message is displayed on the wall in browse tab
driver.save_screenshot('./result/postmsg_case_3_6.png')

writer_browse = driver.find_element_by_xpath("//*[@id=\"msgWall_browse\"]/div[2]/div/div[1]/div")
postedMsg_browse = driver.find_element_by_xpath("//*[@id=\"msgWall_browse\"]/div[2]/div/div[2]/div[1]/div")

f.write(str(step_num)+'. '+'The latest message is posted ')
f.write(common.compareText("From: abc@abc",writer_browse.text,"writer"))
f.write(common.compareText(content,postedMsg_browse.text,"post message"))
step_num+= 1

# Go back to home tab and refresh
home_tab = driver.find_element_by_id("tab_home")
refresh_button_home = driver.find_element_by_id("refresh")

home_tab.click()
f.write(str(step_num)+'. '+'Go back to home tab\n')
step_num+= 1

refresh_button_home.click()
f.write(str(step_num)+'. '+'Click the Refresh button\n')
step_num+= 1

# The wall should display the message posted in browse tab

driver.save_screenshot('./result/postmsg_case_3_7.png')
writer_home = driver.find_element_by_xpath("//*[@id=\"msgWall\"]/div[2]/div/div[1]/div")
postedMsg_home = driver.find_element_by_xpath("//*[@id=\"msgWall\"]/div[2]/div/div[2]/div[1]/div")


f.write(str(step_num)+'. '+'Message posted in browse tab is displayed in home tab ')
step_num+= 1
f.write(common.compareText("From: abc@abc",writer_home.text,"writer"))
f.write(common.compareText(content,postedMsg_home.text,"post message"))


# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()
