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
    
    try:
        # Navegar a la página de Super Mami Argentina
        driver.get("https://www.supermami.com.ar/super/home")

        print("---------- Super Mami ----------")

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

                print("Precio actual del producto buscado: " + precio_actual)
                print("Precio anterior del producto buscado: " + precio_anterior)
            elif len(precios) >= 1:
                precio_actual = precios[0].text.strip()

                print("Precio actual del producto buscado: " + precio_actual)
                print("El producto no tiene descuentos")
            else:
                print("No se encontraron precios para el producto buscado.")

        except:
            print("Producto no encontrado")

    except Exception as e:
        print("Error al conectar con la página web:", e)
        print("Asegúrate de tener conexión a Internet y que la URL sea correcta.")

    # Cerrar el navegador
    driver.quit()