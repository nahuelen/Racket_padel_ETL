# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup as bs
#%%
driver= webdriver.Chrome()
driver.get("https://padelusa.com/")
driver.implicitly_wait(1)
buscar_padelusa= driver.find_element(By.ID,"search-model-input")
buscar_padelusa.click()
buscar_padelusa.send_keys("Wilson bela", Keys.ENTER)
htlm= driver.page_source
#%%
soup= bs(htlm,'lxml')
print(soup)
#%%
driver1= webdriver.Chrome()
driver1.get("https://www.casaspadel.com/es")
driver1.implicitly_wait(1)
buscar_casaspadel= driver1.find_element(By.CLASS_NAME,"icon-search")
buscar_casaspadel.click()
buscar_casapadel1=driver1.find_element(By.CLASS_NAME,"site-header__search-input")
buscar_casapadel1.send_keys("Wilson bela")
buscar_casapadel1.send_keys(Keys.ENTER)
#%%
driver2= webdriver.Chrome()
driver2.get("https://racketcentral.com/pages/padel")
driver2.implicitly_wait(1)
buscar_racketcentral= driver2.find_element(By.CLASS_NAME,'js-search-input')
buscar_racketcentral.click()
buscar_racketcentral.send_keys("Wilson bela")
buscar_racketcentral.send_keys(Keys.ENTER)
