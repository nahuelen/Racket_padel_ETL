import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
#%%
driver= webdriver.Chrome()
url="https://padelusa.com/collections/padel-rackets"
driver.get(url)
driver.implicitly_wait(1)
htlm= driver.page_source
soup= bs(htlm,'lxml')
articulos= soup.find('ul',{'id':'product-grid'}).find_all('a')
id_paletas=[a.get('href')for a in articulos]
paletas_padel_usa= pd.Series()
def scrapear_paletas (id_paletas):
    print('/n paleta:' + id_paletas)
    url= 'https://padelusa.com/'+id_paletas
    driver.get(url)
    htlm= driver.page_source
    soup= bs(htlm,'lxml')
    nombre= soup.find('div',{'class':'product__title'}).text
    #print('\n nombre:'+ nombre)
    precio= soup.find('span',
                      {'class':'price-item price-item--sale price-item--last'}).text.replace('.',',')
    #print('\n precio:'+ precio)
    marca=soup.find('a',{'class':'product__text inline-richtext vendor'}).text
    #print('\n marca:'+ marca)
    paletas_padel_usa['Nombre']=nombre
    paletas_padel_usa['Precio']=precio
    paletas_padel_usa['Marca']= marca
    df_paletas_padel_usa= pd.DataFrame(paletas_padel_usa)
    return(df_paletas_padel_usa.T)
    
id_paletas=pd.DataFrame(id_paletas)
id_paletas.columns=['id']
print(id_paletas)

df_paletas_padel_usa= scrapear_paletas(id_paletas.iloc[0].id)
for index, row in id_paletas.iterrows():
    df_paletas_padel_usa = pd.concat(
        [df_paletas_padel_usa, scrapear_paletas(row['id'])]
    )

#%%
print(df_paletas_padel_usa)
df_paletas_padel_usa = df_paletas_padel_usa.drop_duplicates()
df_paletas_padel_usa['Precio']=df_paletas_padel_usa['Precio'].str.replace('$','')
df_paletas_padel_usa.to_excel('padel_usa.xlsx')