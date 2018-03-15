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
f = common.createFileObj('signup_case_5')
scenario = 'Scenario: Sign up successfully'
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
email.send_keys("dummy3@gmail.com")
password.send_keys("abcd1234")
repeatpsw.send_keys("abcd1234")

f.write(str(step_num)+'. '+'Fill in all signup information\n')
step_num+= 1

driver.save_screenshot('./result/signup_case_5_1.png')

signup_button = driver.find_element_by_id("btn_signup")
signup_button.click()
f.write(str(step_num)+'. '+'Click the Sign Up button\n')
step_num+= 1

# Feedback from server
msgtext = "Successfully created a new user."
msgtext2 = "You may try your first login."

f.write(str(step_num)+'. '+'Sign up a new user - '+msgtext+"\n")
step_num+= 1

errormsg = driver.find_element_by_id("errormsgSignUp")
loginmsg = driver.find_element_by_id("loginmsg")
f.write(common.compareText(msgtext,errormsg.text,"error message"))
f.write(common.compareText(msgtext2,loginmsg.text,"login message"))

# End of the test
driver.quit()
f.write(str(step_num)+'. '+'Close the browser\n\n')
step_num+= 1
common.printTestResult(f,result)
f.close()

