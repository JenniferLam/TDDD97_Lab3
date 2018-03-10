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
f = common.createFileObj('changepw_case_1')
scenario = 'Scenario: Change password with old password'
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

driver.save_screenshot('./result/changepw_case_1_1.png')
	
# To make sure if the user is as same as sign in username
email = driver.find_element_by_name("home_personalInfo_email")
f.write(str(step_num)+'. '+'Verify the username ')
step_num+= 1

if email.text != "abc@abc":
	result = False
	f.write('(WRONG USER): '+email.text)
f.write('\n')

# Go to account tab
account_tab = driver.find_element_by_id("tab_account")
account_tab.click()
f.write(str(step_num)+'. '+'Go to Account Tab\n')
step_num+= 1

oldPW = driver.find_element_by_name("oldPW")
newPW = driver.find_element_by_name("newPW")
confirmPW = driver.find_element_by_name("confirmPW")

# Fill in wrong old password
oldPW.send_keys("abce1234")
newPW.send_keys("qwer1234")
confirmPW.send_keys("qwer1234")
f.write(str(step_num)+'. '+'Fill in wrong old password\n')
step_num+= 1

changePW_button = driver.find_element_by_id("changePWBtn")
changePW_button.click()
f.write(str(step_num)+'. '+'Click the ChangePW button\n')
step_num+= 1

driver.save_screenshot('./result/changepw_case_1_2.png')

errormsg = driver.find_element_by_id("errormsgPW")
msgtext = "Wrong password."

f.write(str(step_num)+'. '+'Verify the error message - ')
step_num+= 1

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+ errormsg.text)
f.write('\n')

# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()
