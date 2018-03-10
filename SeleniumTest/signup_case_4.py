from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import common

# Create chrome webdriver
driver = webdriver.Chrome()

# Test Case Information
result = True
step_num = 1
f = common.createFileObj('signup_case_4')
scenario = 'Scenario: Sign up with password validation'
precondition = 'Pre-condition: The user did not sign up before'
common.printTitle(f, scenario, precondition)

# Go to Twidder
driver.get("http://127.0.0.1:5000")
f.write(str(step_num)+'. '+'Open the browser\n')
step_num+= 1

firstname = driver.find_element_by_name("firstname")
familyname = driver.find_element_by_name("familyname")
gender = Select(driver.find_element_by_tag_name("select"))
city = driver.find_element_by_name("city")
country = driver.find_element_by_name("country")
email = driver.find_element_by_id("signup_email")
password = driver.find_element_by_name("passwordSignUp")
repeatpsw = driver.find_element_by_name("repeatPSW")

# Fill in the sign up information and submit
firstname.send_keys("dummy")
familyname.send_keys("dummy")
gender.select_by_visible_text("Male")
city.send_keys("HK")
country.send_keys("HK")
email.send_keys("dummy1@gmail.com")

f.write(str(step_num)+'. '+'Fill in all signup information\n')
step_num+= 1

# Fill in the password (not fulfil the min length of characters)
password.send_keys("abcd123")
repeatpsw.send_keys("abcd1234")

f.write(str(step_num)+'. '+'Fill in the password less than 8 characters\n')
step_num+= 1

signup_button = driver.find_element_by_id("btn_signup")
signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

# Error message is expected
driver.save_screenshot('./result/signup_case_4_1.png')
errormsg = driver.find_element_by_id("errormsgSignUp")
msgtext = "The password should have at least 8 characters."
f.write(str(step_num)+'. '+'Verify error message - '+msgtext)
step_num+= 1

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Fill in a different password in repeatPSW
password.clear()
repeatpsw.clear()
password.send_keys("abcd1234")
repeatpsw.send_keys("qwer1234")

f.write(str(step_num)+'. '+'Fill in the different password in repeatPSW \n')
step_num+= 1


signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

driver.save_screenshot('./result/signup_case_4_2.png')
msgtext = "The password must be the same."

f.write(str(step_num)+'. '+'Verify error message - '+msgtext)
step_num+= 1

if errormsg.text != msgtext :
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()

