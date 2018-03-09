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
f = common.createFileObj('signin_case_4')
scenario = 'Scenario: Sign in with invalid email'
precondition = 'Pre-condition: The user did not sign in before'
common.printTitle(f, scenario, precondition)

# Go to Twidder
driver.get("http://127.0.0.1:5000")
f.write(str(step_num)+'. '+'Open the browser\n')
step_num+= 1

username = driver.find_element_by_id("signin_email")
password = driver.find_element_by_id("signin_pw")

# Fill in the username with invalid email format
username.send_keys("abcabc")
f.write(str(step_num)+'. '+'Fill in the username with invalid email format\n')
step_num+= 1

password.send_keys("abcd1234")
f.write(str(step_num)+'. '+'Fill in the password\n')
step_num+= 1

# Error message is expected
signin_button = driver.find_element_by_id("btn_signin")
signin_button.click()
f.write(str(step_num)+'. '+'Click the Sign In button\n')
step_num+= 1
driver.implicitly_wait(3)

errormsg = driver.find_element_by_id("errormsgSignIn")
f.write(str(step_num)+'. '+'Verify the error message ')
step_num+= 1

driver.save_screenshot('./result/signin_case_4_1.png')

if errormsg.text != "Please type valid email address.":
	result = False
	f.write('(WRONG ERROR MESSAGE)')

f.write('\n')

# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()




