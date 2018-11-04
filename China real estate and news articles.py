#!/usr/bin/env python
# coding: utf-8

# In[12]:


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd

driver = webdriver.Chrome("C:/Users/w0bin/chromedriver.exe")

# keywords to loop through
keywords = ["Claims", "Manipulate", "Questionable", "Stagnant", "Distressed", "Understate", "Outperformed", "Favourable", "Consistent", "Poised"]
searchResults = {}
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #, 11, 12]
days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
#years = [2011, 2012, 2013, 2014, 2015, 2016, 2017]
saved_year = 0

firstLoopDone = False
savedYear = 0
date = ""

# to change number of month into string
def getMonth(month_int):
    switcher = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    return switcher.get(month_int, "Dec")
for month in months:
    for day in days:
        date = str(day) + "/" + str(month) + "/" + "2018"
        searchResults.setdefault("Date", []).append(date)    
 
for keyword in keywords:
    driver.get('https://www.google.com/')
    #elem = driver.find_element_by_id("lst-ib")
    #elem.clear()
    elem = driver.find_element_by_id("lst-ib") 
    elem.send_keys("china real estate" + " " + keyword)
    elem.send_keys(Keys.RETURN)
    driver.find_element_by_partial_link_text('News').click()
    for month in months:
        savedMonth = month-1 # to ensure the next month loop can access the previous month
        for day in days:
            driver.find_element_by_id("hdtb-tls").click() # click on tools
            if firstLoopDone == False:
                firstKey = 'Recent'
                firstLoopDone = True
            elif (day == 1) and (savedMonth != 0):
                firstKey = "28" + " " + str(getMonth(savedMonth)) + " " + "2018"
            else:
                firstKey = str(day-1) + " " + str(getMonth(month)) + " " + "2018"
            time.sleep(3)
            #driver.find_element_by_id("gsr").click() # click on drop down "Recent"
            print('select ok')
            elem_driver = driver.find_element_by_xpath("//div[@aria-label='" + firstKey + "']/div[@class='mn-hd-txt']")
            elem_driver.click()
            print('select date ok')
            driver.find_element_by_id("cdrlnk").click()
            driver.find_element_by_id("cdr_min").clear()
            driver.find_element_by_id("cdr_max").clear()
            date_from = driver.find_element_by_id("cdr_min")
            date_from.send_keys(str(month) + "/" + str(day) +"/" + "2018")
            date_to = driver.find_element_by_id("cdr_max")
            date_to.send_keys(str(month) +"/" + str(day) +"/" + "2018")
            date_to.send_keys(Keys.RETURN)

            driver.find_element_by_id("hdtb-tls").click()
            time.sleep(2)
            results = driver.find_element_by_id("resultStats").text
            search = results[results.find("t ")+1:results.find(" r")].strip()
            search = search.replace(",", "")
            print(search)
            searchResults.setdefault(keyword, []).append(search)
            time.sleep(5)
    # to reset retrieval for new keyword
    if month == 10:
        firstLoopDone = False
            
print(searchResults)
df = pd.DataFrame(searchResults)
df

