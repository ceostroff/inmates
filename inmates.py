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

# function to get the links for the first page that uses html
def getLinks(pageVals):
    global driver
    #go down the page to the section with this class
    pageSection = driver.find_element_by_class_name("dcCSStableLight")
    # find the a tags within a specific table
    pageNav = pageSection.find_elements_by_xpath("/html/body/div/div/div/table/tbody/tr/td/table/tbody/tr/td/a")
    #for each a tag among these a tags
    for pageLink in pageNav:
        #get the href (the url) and add it to the list called pagesVals
        pageVals.append(pageLink.get_attribute('href'))   
        
#function to get the links for all pages after the first        
def getPages(pageVals):
    global driver
    #variable instructs the driver to find the button on the page
    button = driver.find_element_by_xpath("//input[@name='rsOffenderRoot_PagingMove' and @value='Next']")
    #while the button exists, run a loop. this will keep running until the button no longer exists
    while True:
        try:
            #wait for the page to load and after a certain amount of time has passed, find the button
            button = WebDriverWait(driver, 5, 0.25).until(EC.visibility_of_element_located([By.XPATH, "//input[@name='rsOffenderRoot_PagingMove' and @value='Next']"]))
            #click the button
            button.click()
            #take a break. even scrapers get tired
            time.sleep(3)
            #same thing from get links: find the part of the page with this class
            pageSection = driver.find_element_by_class_name("dcCSStableLight")
            #find the a tags in the table
            pageNav = pageSection.find_elements_by_xpath("/html/body/div/div/div/table/tbody/tr/td/table/tbody/tr/td/a")
            #for each page, get all of the a tags
            for pageLink in pageNav:
                #for each of those links, get the href and add it to the same list called pageVals
                pageVals.append(pageLink.get_attribute('href'))
            #run this function over and over, doing this for each page UNLESS it no longer works, in which case break the loop
        except:
            break
    
        
#function to get the demographic information for each inmate    
def getDetails(pageVals):
    global driver
    global inmates
    #for each link in the list you have stored in pageVals
    for value in pageVals:
        #open each link
        html = urlopen(value)
        #we're using BeautifulSoup to scrape
        bsObj = BeautifulSoup(html, "html.parser")
        #find all of the td tags within a table 
        td_list = bsObj.findAll("td", {"align":"LEFT"})
        #make a python dictionary, assigning a key and for each key, an attribute. Because these tags make have weird spacing, get their text and strip all formatting. This makes it easier to use when we export to a CSV
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
        #make a new python list called inmates and append your python dictionary, inmate, to that
        inmates.append(inmate)
        
#function to save all of your hard work to a CSV        
def saveToCSV(inmates):
    global driver
    #give the csv file you want to export it to a name
    filename = 'inmates.csv' 
    #open your new csv file with a 'w' so you can write to it
    with open(filename, 'w') as output_file:
        #make headers for you columns. these must match up with the keys you set in your python dictionary, inamte
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
        #write these into a csv, the headers being fieldnames and the rows your list of inmates
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inmates)
#you prefered driver has to open the original page to do all this. I use Firefox here but Chrome is also an option        
driver = webdriver.Firefox()
driver.get("http://www.dc.state.fl.us/activeinmates/list.asp?dataaction=GetInst&facility2=279")
#your lists where info will be stored
pageVals = []
inmates = []
#run the functions, using the values (links) of the lists we created        
getLinks(pageVals) 
getPages(pageVals) 
driver.close() # close the driver 

getDetails(pageVals)
saveToCSV(inmates)


#Ta-Da!    
