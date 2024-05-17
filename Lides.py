import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options

def scrape_farmacia_lider(codigo_barra):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    
    url = f"https://farmaciaslider.com.ar/busqueda?controller=search&s={codigo_barra}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        nombreProducto = soup.find_all('h3', class_='h3 product-title')
        precios = soup.find_all('div', class_='product-price-and-shipping')
        
        
        print("---------- Lider ----------")
        if nombreProducto:
            # Itera sobre los resultados para obtener el nombre y el precio de cada producto
            for i in range(len(nombreProducto)):
                nombre = nombreProducto[i].text.strip()

                # Encuentra los precios actuales y regulares
                precio_actual = precios[i].find('span', class_='product-price').text.strip()
                precio_regular = precios[i].find('span', class_='regular-price text-muted').text.strip()

                print(f"Nombre: {nombre}")
                print(f"Precio actual: {precio_actual}")
                print(f"Precio regular: {precio_regular}")
        else:
            print("No se encontraron resultados.")
    else:
        print("Error al obtener la página.")

        
