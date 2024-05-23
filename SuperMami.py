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

def buscador_superMami(codigo_barras):
    options = Options()
    options.add_argument("--headless")
    
    driver = webdriver.Firefox(options=options)
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}
    
    try:
        # Navegar a la página de Super Mami Argentina
        driver.get("https://www.supermami.com.ar/super/home")

        boton = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn.btn-nobg.getFullSearch"))
        )

        # Hacer clic en el botón
        boton.click()

        # Pegar el código de barras directamente en el campo de búsqueda
        campo_busqueda = driver.find_element(By.ID, "searchText")
        campo_busqueda.send_keys(codigo_barras)
        campo_busqueda.submit()

        time.sleep(3)  
        
        try:
            # Esperar a que se carguen los resultados de búsqueda
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.precio-unidad"))
            )

            # Encontrar los elementos que contienen los precios del producto buscado
            precios = driver.find_elements(By.CSS_SELECTOR, "div.precio-unidad span")

            if len(precios) >= 2:
                precio_actual = precios[0].text.strip()
                precio_anterior = precios[1].text.strip()

                salida = {"producto": "Producto", "precio_actual": precio_actual, "precio_anterior": precio_anterior}
                driver.quit()
                return salida
                

            elif len(precios) >= 1:
                precio_actual = precios[0].text.strip()

                # El producto no tiene descuentos
                salida = {"producto": "Producto", "precio_actual": precio_actual, "precio_anterior": precio_actual}
                driver.quit()
                return salida
                
            else:
                # No se encontraron precios para el producto buscado
                driver.quit()
                return salida

        except:
            # Producto no encontrado
            driver.quit()
            return salida

    except Exception as e:
        # Error al conectar con la página web
        # Asegúrate de tener conexión a Internet y que la URL sea correcta.
        driver.quit()
        return salida