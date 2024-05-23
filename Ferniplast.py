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

def buscador_ferniplast(codigo_barra):
    options = Options()
    options.add_argument("--headless") 
    driver = webdriver.Firefox(options=options)
    
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}
    
    try:
        # Navegar a la página de Ferniplast
        driver.get("https://www.ferniplast.com/")
        
        campo_busqueda = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "downshift-0-input"))
        )
        campo_busqueda.click
        campo_busqueda.send_keys(codigo_barra)
        campo_busqueda.send_keys(Keys.RETURN)

        time.sleep(5) 
        
        try:
            not_found_element = driver.find_elements(By.CSS_SELECTOR, ".vtex-rich-text-0-x-container.vtex-rich-text-0-x-container--not-found.flex.tl.items-start.justify-start.t-body.c-on-base")
            # Esperar a que se cargue la página de resultados
            
            if not_found_element:
                # Producto no encontrado
                driver.quit()
                return salida
            
            else:
                time.sleep(3)  
                
                precio_actual = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.vtex-store-components-3-x-sellingPriceValue.vtex-product-summary-2-x-sellingPrice.vtex-product-summary-2-x-sellingPrice--product-box"))
                )

                precio_completo = precio_actual.text

                # Verificar si hay un precio sin descuento
                precio_lista_element = driver.find_elements(By.CSS_SELECTOR, "span.vtex-store-components-3-x-listPriceValue.vtex-product-summary-2-x-listPrice.vtex-product-summary-2-x-listPrice--product-box.strike")

                if precio_lista_element:
                    precio_lista = precio_lista_element[0].text
                    salida = {"producto": "Producto", "precio_actual": precio_completo, "precio_anterior": precio_lista}
                    driver.quit()
                    return salida
                else:
                    # No hay precio con descuento disponible
                    salida = {"producto": "Producto", "precio_actual": precio_completo, "precio_anterior": precio_completo}
                    driver.quit()
                    return salida
            
        except TimeoutException:
            driver.quit()
            return salida
            

    except TimeoutException:
        driver.quit()
        return salida


                    