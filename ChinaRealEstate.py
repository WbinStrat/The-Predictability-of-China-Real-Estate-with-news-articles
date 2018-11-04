#!/usr/bin/env python
# coding: utf-8

# In[67]:


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd

driver = webdriver.Chrome("C:/Users/w0bin/chromedriver.exe")

# keywords to loop through
keywords = ["claims", "manipulate", "questionable", "stagnant", "distressed", "understate", "outperformed", "favourable", "consistent"]
searchResults = {}
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
years = [2011, 2012, 2013, 2014, 2015, 2016, 2017]
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
for year in years:
    for month in months:
        date = "1/" + str(month) + "/" + str(year)
        searchResults.setdefault("Date", []).append(date)    
 
for keyword in keywords:
    driver.get('https://www.google.com/')
    #elem = driver.find_element_by_id("lst-ib")
    #elem.clear()
    elem = driver.find_element_by_id("lst-ib") 
    elem.send_keys("china real estate" + " " + keyword)
    elem.send_keys(Keys.RETURN)
    driver.find_element_by_partial_link_text('News').click()
    for year in years:
        savedYear = year-1 # to ensure the next year loop can access the previous year
        for month in months:
            driver.find_element_by_id("hdtb-tls").click() # click on tools
            if firstLoopDone == False:
                firstKey = 'Recent'
                firstLoopDone = True
            elif (month == 1) and (savedYear != 2010):
                firstKey = "1" + " " + str(getMonth(month-1)) + " " + str(savedYear)
            else:
                firstKey = "1" + " " + str(getMonth(month-1)) + " " + str(year)
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
            date_from.send_keys(str(month) + "/" +"1/" + str(year))
            date_to = driver.find_element_by_id("cdr_max")
            date_to.send_keys(str(month) +"/" +"1/" + str(year))
            date_to.send_keys(Keys.RETURN)

            driver.find_element_by_id("hdtb-tls").click()
            results = driver.find_element_by_id("resultStats").text
            search = results[results.find("t ")+1:results.find(" r")].strip()
            search = search.replace(",", "")
            print(search)
            searchResults.setdefault(keyword, []).append(search)
            time.sleep(5)
    # to reset retrieval for new keyword
    if year == 2017:
        firstLoopDone = False
            
print(searchResults)
df = pd.DataFrame(searchResults)
df

