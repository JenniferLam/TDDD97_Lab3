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
f = common.createFileObj('signin_case_2')
scenario = 'Scenario: Sign in with wrong username and password'
precondition = 'Pre-condition: The user did not sign in before'
common.printTitle(f, scenario, precondition)

# Go to Twidder
driver.get("http://127.0.0.1:5000")
f.write(str(step_num)+'. '+'Open the browser\n')
step_num+= 1

# Fill in the username and password
username = driver.find_element_by_id("signin_email")
password = driver.find_element_by_id("signin_pw")

# Wrong Username
username.send_keys("xxx@xxx")
f.write(str(step_num)+'. '+'Fill in the wrong username\n')
step_num+= 1

password.send_keys("abcd1234")
f.write(str(step_num)+'. '+'Fill in the password\n')
step_num+= 1

# Error message is expected
signin_button = driver.find_element_by_id("btn_signin")
signin_button.click()
f.write(str(step_num)+'. '+'Click the Sign In button\n')
step_num+= 1

driver.save_screenshot('./result/signin_case_2_1.png')

msgtext = "Wrong username or password."
f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1
errormsg = driver.find_element_by_id("errormsgSignIn")
if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Correct the username but fill in wrong password
# Wrong Username
username.send_keys("abc@abc")
f.write(str(step_num)+'. '+'Fill in the username\n')
step_num+= 1

password.send_keys("abcd12")
f.write(str(step_num)+'. '+'Fill in the wrong password\n')
step_num+= 1

driver.save_screenshot('./result/signin_case_2_2.png')

msgtext = "Wrong username or password."
f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()




