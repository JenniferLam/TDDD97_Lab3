from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import common

# Create chrome webdriver
driver = webdriver.Chrome()

# Test Case Information
result = True
step_num = 1
f = common.createFileObj('signin_case_3')
scenario = 'Scenario: Sign in with missing username or password'
precondition = 'Pre-condition: The user did not sign in before'
common.printTitle(f, scenario, precondition)

# Go to Twidder
driver.get("http://127.0.0.1:5000")
f.write(str(step_num)+'. '+'Open the browser\n')
step_num+= 1

username = driver.find_element_by_id("signin_email")
password = driver.find_element_by_id("signin_pw")

# Leave the username and password empty
# Error message is expected
signin_button = driver.find_element_by_id("btn_signin")
signin_button.click()
f.write(str(step_num)+'. '+'Click the Sign In button\n')
step_num+= 1
driver.implicitly_wait(3)


f.write(str(step_num)+'. '+'Verify the error message ')
step_num+= 1

driver.save_screenshot('./result/signin_case_3_1.png')
errormsg = driver.find_element_by_id("errormsgSignIn")
if errormsg.text != "Please type your email.":
	result = False
	f.write('(WRONG ERROR MESSAGE)')

f.write('\n')

# Only fill in the username
username.send_keys("abc@abc")
f.write(str(step_num)+'. '+'Fill in the username\n')
step_num+= 1

password.clear()
f.write(str(step_num)+'. '+'No password\n')
step_num+= 1


# Error message is expected

signin_button.click()
f.write(str(step_num)+'. '+'Click the Sign In button\n')
step_num+= 1
driver.implicitly_wait(3)


f.write(str(step_num)+'. '+'Verify the error message ')
step_num+= 1

driver.save_screenshot('./result/signin_case_3_2.png')

if errormsg.text != "Please type your password.":
	result = False
	f.write('(WRONG ERROR MESSAGE)')

f.write('\n')

# Only fill in the password
username.clear()
f.write(str(step_num)+'. '+'No username\n')
step_num+= 1

password.send_keys("abcd1234")
f.write(str(step_num)+'. '+'Fill in the password\n')
step_num+= 1

# Error message is expected

signin_button.click()
f.write(str(step_num)+'. '+'Click the Sign In button\n')
step_num+= 1
driver.implicitly_wait(3)


f.write(str(step_num)+'. '+'Verify the error message ')
step_num+= 1

driver.save_screenshot('./result/signin_case_3_3.png')

if errormsg.text != "Please type your email.":
	result = False
	f.write('(WRONG ERROR MESSAGE)')

f.write('\n')

# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()




