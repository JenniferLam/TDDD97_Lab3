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
f = common.createFileObj('signup_case_1')
scenario = 'Scenario: Sign up with missing information'
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

# Leave all fields empty
f.write(str(step_num)+'. '+'Leave all fields empty\n')
step_num+= 1
signup_button = driver.find_element_by_id("btn_signup")
signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

errormsg = driver.find_element_by_id("errormsgSignUp")
msgtext = "Please type your first name."
f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1

driver.save_screenshot('./result/signup_case_1_1.png')

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Fill in the first name
firstname.send_keys("dummy")
f.write(str(step_num)+'. '+'Fill in the first name\n')
step_num+= 1

signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

msgtext = "Please type your family name."
f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1

driver.save_screenshot('./result/signup_case_1_2.png')

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Fill in the family name
familyname.send_keys("dummy")
f.write(str(step_num)+'. '+'Fill in the family name\n')
step_num+= 1

signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

msgtext = "Please select your gender."
f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1

driver.save_screenshot('./result/signup_case_1_3.png')

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Select the gender
gender.select_by_visible_text("Male")
f.write(str(step_num)+'. '+'Select the gender\n')
step_num+= 1

signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

msgtext = "Please type your city."
f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1

driver.save_screenshot('./result/signup_case_1_4.png')

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Fill in the city
city.send_keys("HK")
f.write(str(step_num)+'. '+'Fill in the city\n')
step_num+= 1

signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

msgtext = "Please type your country."
f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1

driver.save_screenshot('./result/signup_case_1_5.png')

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Fill in the country
country.send_keys("HK")
f.write(str(step_num)+'. '+'Fill in the country\n')
step_num+= 1

signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

msgtext = "Please type your email."
f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1

driver.save_screenshot('./result/signup_case_1_6.png')

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Fill in the email
email.send_keys("dummy@gmail.com")
f.write(str(step_num)+'. '+'Fill in the email\n')
step_num+= 1

signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

msgtext = "Please type your password."
f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1

driver.save_screenshot('./result/signup_case_1_7.png')

if errormsg.text != msgtext :
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Fill in the password
password.send_keys("abcd1234")
f.write(str(step_num)+'. '+'Fill in the password\n')
step_num+= 1

signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

msgtext = "Please confirm your password."

f.write(str(step_num)+'. '+'Verify the error message - '+msgtext)
step_num+= 1

driver.save_screenshot('./result/signup_case_1_8.png')

if errormsg.text != msgtext:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# Fill in the repeatpsw
repeatpsw.send_keys("abcd1234")
f.write(str(step_num)+'. '+'Fill in the repeatPSW\n')
step_num+= 1

signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

# Sign up successfully
msgtext = "Successfully created a new user."
msgtext2 = "You may try your first login."

f.write(str(step_num)+'. '+'Sign up a new user - '+msgtext)
step_num+= 1

driver.save_screenshot('./result/signup_case_1_9.png')

loginmsg = driver.find_element_by_id("loginmsg")
if errormsg.text != msgtext or loginmsg.text != msgtext2:
	result = False
	f.write('(WRONG ERROR MESSAGE): '+errormsg.text)

f.write('\n')

# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()




