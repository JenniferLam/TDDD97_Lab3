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
f = common.createFileObj('searchUser_case_1')
scenario = 'Scenario: Search non-exist user in browse tab'
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

driver.save_screenshot('./result/searchuser_case_1_1.png')
	
# To make sure if the user is as same as sign in username
email = driver.find_element_by_name("home_personalInfo_email")
f.write(str(step_num)+'. '+'Verify the username ')
f.write(common.compareText("abc@abc",email.text,"username"))
step_num+= 1

# Go to browse tab
browse_tab = driver.find_element_by_id("tab_browse")
browse_tab.click()
f.write(str(step_num)+'. '+'Go to Browse Tab\n')
step_num+= 1

# Search with non-exist email address
searchBar = driver.find_element_by_name("searchEmail")
target_user = "xxxx"
searchBar.send_keys(target_user)
f.write(str(step_num)+'. '+'Type a non-exist email address\n')
step_num+= 1

search_button = driver.find_element_by_id("searchBtn")
search_button.click()
f.write(str(step_num)+'. '+'Click the Search Button\n')
step_num+= 1

msgtext = "No such user."
driver.save_screenshot('./result/searchuser_case_1_2.png')

f.write(str(step_num)+'. '+'Verify error message - '+msgtext+"\n")
step_num+= 1

errormsg = driver.find_element_by_id("errorMsgSearch")
f.write(common.compareText(msgtext,errormsg.text,"error message"))

# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()


