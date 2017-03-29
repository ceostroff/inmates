from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time
import csv

def getLinks(pageVals):
    global driver
    pageSection = driver.find_element_by_class_name("dcCSStableLight")
    pageNav = pageSection.find_elements_by_xpath("/html/body/div/div/div/table/tbody/tr/td/table/tbody/tr/td/a")
    for pageLink in pageNav:
        pageVals.append(pageLink.get_attribute('href'))
    #nextLinks = pageSection.find_elements_by_tag("/html/body/div/div/div/table/tbody/tr/td/form[input/@value='Next']").click()
    #for nextLink in nextLinks:
        #pageVals.append(nextLink.get_attributes('href'))
        #time.sleep(3)    
        
def getPages(pageVals):
    global driver
    button = driver.find_element_by_xpath("//input[@name='rsOffenderRoot_PagingMove' and @value='Next']")
    while True:
        try:
            button = WebDriverWait(driver, 5, 0.25).until(EC.visibility_of_element_located([By.XPATH, "//input[@name='rsOffenderRoot_PagingMove' and @value='Next']"]))
            button.click()
            time.sleep(3)
            pageSection = driver.find_element_by_class_name("dcCSStableLight")
            pageNav = pageSection.find_elements_by_xpath("/html/body/div/div/div/table/tbody/tr/td/table/tbody/tr/td/a")
            for pageLink in pageNav:
                pageVals.append(pageLink.get_attribute('href'))
        except:
            break
    
        
    
def getDetails(pageVals):
    global driver
    global inmates
    for value in pageVals:
        html = urlopen(value)
        bsObj = BeautifulSoup(html, "html.parser")
        td_list = bsObj.findAll("td", {"align":"LEFT"})
        inmate = {
            'id': td_list[0].get_text().strip(),
            'name': td_list[1].get_text().strip(),
            'race': td_list[2].get_text().strip(),
            'sex': td_list[3].get_text().strip(),
            'dob': td_list[9].get_text().strip(),
            'entry': td_list[10].get_text().strip(),
            'facility': td_list[11].get_text().strip(),
            'custody': td_list[12].get_text().strip(),
            'release': td_list[13].get_text().strip(),            
        }
        
        inmates.append(inmate)
        
        
def saveToCSV(inmates):
    global driver
    filename = 'inmates.csv' 
    with open(filename, 'w') as output_file:
        fieldnames = [	'id',
                      'name',
                      'race',
                      'sex',
                      'dob',
                      'entry',
                      'facility',
                      'custody',
                      'release',
                     ]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inmates)
        
driver = webdriver.Firefox()
driver.get("http://www.dc.state.fl.us/activeinmates/list.asp?dataaction=GetInst&facility2=279")
pageVals = []
inmates = []
        
getLinks(pageVals) 
getPages(pageVals) 
driver.close() # close the driver 

getDetails(pageVals)
saveToCSV(inmates)

    