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

def buscador_carrefour(codigo_barras):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}
    driver.get("https://www.carrefour.com.ar/")

    time.sleep(2)
    search_box = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input.vtex-styleguide-9-x-input.ma0.border-box.vtex-styleguide-9-x-hideDecorators.vtex-styleguide-9-x-noAppearance.br2.br-0.br--left.w-100.bn.outline-0.bg-base.c-on-base.b--muted-4.hover-b--muted-3.t-body.pl5"))
    )

    try:
        search_box.clear()
        search_box.send_keys(codigo_barras)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)
    
    except StaleElementReferenceException:
        search_box = driver.find_element(By.CSS_SELECTOR, "input.vtex-styleguide-9-x-input.ma0.border-box.vtex-styleguide-9-x-hideDecorators.vtex-styleguide-9-x-noAppearance.br2.br-0.br--left.w-100.bn.outline-0.bg-base.c-on-base.b--muted-4.hover-b--muted-3.t-body.pl5")
        search_box.clear()
        search_box.send_keys(codigo_barras)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

    driver.implicitly_wait(3)

    try:
        price_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.valtech-carrefourar-product-price-0-x-sellingPrice"))
        )

        try:
            old_price_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.valtech-carrefourar-product-price-0-x-listPrice"))
            )
            
            if price_element:
                price = price_element.get_attribute("textContent")
                old_price = old_price_element.get_attribute("textContent")
                salida = {"producto": "Producto", "precio_actual": price, "precio_anterior": old_price}
                driver.quit()
                return salida
                
        except TimeoutException:
            price = price_element.get_attribute("textContent")
            salida = {"producto": "Producto", "precio_actual": price, "precio_anterior": price}
            driver.quit()
            return salida
            
        
    except TimeoutException:
        driver.quit()
        return salida
            
    driver.quit()
    return salida
    