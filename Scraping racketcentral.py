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
driver = webdriver.Chrome()
x = 1
enlaces_acumulados = pd.DataFrame(columns=['Enlace'])
driver.implicitly_wait(5)
while True:
    url = f'https://racketcentral.com/collections/padel-rackets?page={x}'
    driver.get(url)
    htlm = driver.page_source
    soup = bs(htlm, 'lxml')
    
    try:
        pagina_actual = soup.find('span', {'class': 'pagination__page-current font-bold block leading-none'}).text
        if int(pagina_actual) == x:
            
            # Búsqueda de enlaces de artículos
            articulos = soup.find_all('p', {'class': 'card__title font-bold mb-1'})
            id_paletas = [a.find('a').get('href') for a in articulos]
            enlaces_nuevos = pd.DataFrame({'Enlace': id_paletas})
            enlaces_acumulados = pd.concat([enlaces_acumulados, enlaces_nuevos], ignore_index=True)
        else:
            break
    except AttributeError:
        break
    
    x += 1
paletas_racket_central= pd.Series()
driver.implicitly_wait(5)
def scrapear_paletas (enlaces_acumulados):
    url= 'https://racketcentral.com/'+enlaces_acumulados
    driver.get(url)
    htlm= driver.page_source
    soup= bs(htlm,'lxml')
    nombre= soup.find('h1',{'class':'product-title h5'}).text
    precio= soup.find('strong',{'class':'price__current'}).text.replace('.',',')
    marca = soup.find('span',{'class':'product-vendor'}).find('a', href=lambda href: href and href.startswith('/collections/')).text
    paletas_racket_central['Nombre']=nombre
    paletas_racket_central['Precio']=precio
    paletas_racket_central['Marca']= marca
    df_paletas_racket_central= pd.DataFrame(paletas_racket_central)
    return(df_paletas_racket_central.T)
df_paletas_racket_central= scrapear_paletas(enlaces_acumulados.iloc[0].Enlace)
for idex,row in enlaces_acumulados.iterrows():
    df_paletas_racket_central = pd.concat([df_paletas_racket_central, scrapear_paletas(row['Enlace'])])

driver.quit()
#%%
df_paletas_racket_central=df_paletas_racket_central.reset_index(drop=True)
df_paletas_racket_central['Precio']=df_paletas_racket_central['Precio'].str.replace('$', '')
df_paletas_racket_central.to_excel('paletas_racket_central.xlsx')