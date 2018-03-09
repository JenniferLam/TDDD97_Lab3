from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def createFileObj(fileName):
	#timestr = time.strftime("%Y%m%d-%H%M%S")
	#fName = './result/' + fileName + '_' + timestr
	fName = './result/' + fileName
	f = open(fName, 'w')
	return f

def printTitle(f, scenario, precondition):
	f.write(scenario + "\n")
	f.write(precondition + "\n\n")
	f.write('Test Steps:\n\n')

def printTestResult(f,result):

	if result:
		f.write('Test Result: Passed\n')
	else:
		f.write('Test Result: Failed\n')
