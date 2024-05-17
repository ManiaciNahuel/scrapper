import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
def scrape_farmacia_lider(codigo_barra):
    url = f"https://farmaciaslider.com.ar/busqueda?controller=search&s={codigo_barra}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        nombreProducto = soup.find_all('h3', class_='h3 product-title')
        precios = soup.find_all('div', class_='product-price-and-shipping')
        
        
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

        
# Función para leer los códigos de barras desde un archivo Excel

def leer_codigos_desde_excel(archivo_excel):
    try:
        # Lee el archivo Excel y obtiene los códigos de barras de la primera columna
        df = pd.read_excel(archivo_excel, header=None)  # Sin encabezados
        codigos = df.iloc[:, 0].tolist()  # Toma solo la primera columna
        return codigos
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        return []


# Ejemplo de cómo usar las funciones
archivo_excel = "codigos.xlsx"  # Ruta de tu archivo Excel
codigos_barra = leer_codigos_desde_excel(archivo_excel)
for codigo in codigos_barra:
    print(f"Buscando productos para el código de barras: {codigo}")
    print("---------- LIDER ----------")
    scrape_farmacia_lider(codigo)
    print("\n")
