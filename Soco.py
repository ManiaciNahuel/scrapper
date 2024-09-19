import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def buscador_lider(codigo_barra):
    options = Options()
    """ options.add_argument("--headless") """
    driver = webdriver.Firefox(options=options)
    
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}
    
    url = f"https://zocominimercado.com.ar/search/?q={codigo_barra}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        nombreProducto = soup.find_all('h3', class_='h3 product-title')
        precios = soup.find_all('div', class_='product-price-and-shipping')
        
        
        if nombreProducto:
            # Itera sobre los resultados para obtener el nombre y el precio de cada producto
            for i in range(len(nombreProducto)):
                
                # Encuentra los precios actuales y regulares
                precio_actual = precios[i].find('span', class_='product-price').text.strip()
                precio_regular = precios[i].find('span', class_='regular-price text-muted')
                
                if precio_regular:
                    precio_regular_text = precio_regular.text.strip()
                    salida = {"producto": "Producto", "precio_actual": precio_actual, "precio_anterior": precio_regular_text}
                    driver.quit()
                    return salida
                else: 
                    salida = {"producto": "Producto", "precio_actual": precio_actual, "precio_anterior": precio_actual}
                    driver.quit()
                    return salida
                    
        else:
            driver.quit()
            return salida
    else:

        driver.quit()
        return salida
        
    driver.quit()
    return salida


        

