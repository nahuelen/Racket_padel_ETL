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
import random

#%%
nombre=soup.find('h1',{'class':'h2 product-single__title'}).text
marca= soup.find('div',{'class':'product-single__vendor'}).text
precio=soup.find('span',{'class':'product__price'}).text.replace('.',',')
precio=soup.find('span',{'class':'product__price on-sale'}).text.replace('.',',')
#%%
#%%
driver = webdriver.Chrome()
x = 1
enlaces_acumulados = pd.DataFrame(columns=['Enlace'])
driver.implicitly_wait(5)
while True:
    url = f'https://www.casaspadel.com/collections/padel-rackets?page={x}'
    driver.get(url)
    htlm = driver.page_source
    soup = bs(htlm, 'lxml')
    
    try:
        pagina_actual = soup.find('div', {'class': 'pagination'}).find('span', {'class': 'page current'}).text
        if int(pagina_actual) == x:
            
            # Búsqueda de enlaces de artículos
            articulos = soup.find_all('div', {'class': 'grid-product__content'})
            id_paletas = [a.find('a').get('href') for a in articulos]
            enlaces_nuevos = pd.DataFrame({'Enlace': id_paletas})
            enlaces_acumulados = pd.concat([enlaces_acumulados, enlaces_nuevos], ignore_index=True)
        else:
            break
    except AttributeError:
        break
    
    x += 1

paletas_casas_padel= pd.Series()
driver.implicitly_wait(5)
def scrapear_paletas (enlaces_acumulados):
    url= 'https://www.casaspadel.com'+enlaces_acumulados
    driver.get(url)
    htlm= driver.page_source
    soup= bs(htlm,'lxml')
    nombre=soup.find('h1',{'class':'h2 product-single__title'}).text
    precio = ""
    precio_on_sale = soup.find('span', {'class': 'product__price on-sale'})
    if precio_on_sale:
        precio = precio_on_sale.text.replace('.', ',')
    else:
        precio_normal = soup.find('span', {'class': 'product__price'})
        if precio_normal:
            precio = precio_normal.text.replace('.', ',')
    marca= soup.find('div',{'class':'product-single__vendor'}).text
    paletas_casas_padel['Nombre']=nombre
    paletas_casas_padel['Precio']=precio
    paletas_casas_padel['Marca']= marca
    df_paletas_casas_padel= pd.DataFrame(paletas_casas_padel)
    return(df_paletas_casas_padel.T)
df_paletas_casas_padel= scrapear_paletas(enlaces_acumulados.iloc[0].Enlace)
for idex,row in enlaces_acumulados.iterrows():
    df_paletas_casas_padel = pd.concat([df_paletas_casas_padel, scrapear_paletas(row['Enlace'])])
driver.quit()

#%%
df_paletas_casas_padel=df_paletas_casas_padel.reset_index(drop=True)
df_paletas_casas_padel=df_paletas_casas_padel.drop_duplicates()
df_paletas_casas_padel['Precio']=df_paletas_casas_padel['Precio'].str.replace('$', '')
df_paletas_casas_padel.to_excel('paletas_casas_padel.xlsx')

