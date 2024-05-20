from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.firefox.options import Options

def buscador_farmacity(codigo_barra):
    options = Options()
    options.add_argument("--headless") 
    driver = webdriver.Firefox(options=options)
    
    try:
        # Navegar a la página de Farmacity 
        driver.get("https://www.farmacity.com/")

        print("---------- Farmacity ----------")
        
        campo_busqueda = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "downshift-0-input"))
        )
        campo_busqueda.click
        campo_busqueda.send_keys(codigo_barra)
        campo_busqueda.send_keys(Keys.RETURN)

        time.sleep(3)  
        
        try:
            not_found_element = driver.find_elements(By.CLASS_NAME, "farmacityar-store-components-1-x-notFoundText")
            no_stock_element = driver.find_elements(By.CLASS_NAME, "farmacityar-store-components-1-x-no_stock")
            
            # Esperar a que se cargue la página de resultados
            
            if not_found_element:
                print("Producto no encontrado")
            elif no_stock_element:
                print("Producto encontrado pero sin stock disponible")
            else:
                precio_actual = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.vtex-product-price-1-x-sellingPriceValue"))
                )
            
                precio_completo = precio_actual.text
                
                # Verificar si hay un precio sin descuento
                precio_lista_element = driver.find_elements(By.CSS_SELECTOR, "span.vtex-product-price-1-x-listPriceValue.strike")
                
                if precio_lista_element:
                    precio_lista = precio_lista_element[0].text
                    print(f"Precio del producto: {precio_completo}")
                    print(f"Precio sin descuento: {precio_lista}")
                else:
                    print(f"Precio del producto: {precio_completo}")
                    print("No hay precio con descuento disponible")
            
        except TimeoutException:
            print("Producto no encontrado")

    except TimeoutException:
        print("Producto no encontrado")
    
    driver.quit()

