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
    
    # Navegar a la página de Carrefour Argentina
    driver.get("https://www.carrefour.com.ar/")

    # Esperar a que el elemento de búsqueda esté presente y visible
    search_box = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input.vtex-styleguide-9-x-input.ma0.border-box.vtex-styleguide-9-x-hideDecorators.vtex-styleguide-9-x-noAppearance.br2.br-0.br--left.w-100.bn.outline-0.bg-base.c-on-base.b--muted-4.hover-b--muted-3.t-body.pl5"))
    )

    try:
        search_box.clear()
        # Ingresar el código de barras
        search_box.send_keys(codigo_barras)
        # Pequeña pausa antes de enviar la búsqueda
        time.sleep(1)
        
        # Enviar la búsqueda presionando Enter
        search_box.send_keys(Keys.RETURN)
        
    except TimeoutException:
        print("No tiene descuento")
    except StaleElementReferenceException:
        print("El elemento de búsqueda se ha vuelto 'stale', volviendo a encontrarlo")
        search_box = driver.find_element(By.CSS_SELECTOR, "input.vtex-styleguide-9-x-input.ma0.border-box.vtex-styleguide-9-x-hideDecorators.vtex-styleguide-9-x-noAppearance.br2.br-0.br--left.w-100.bn.outline-0.bg-base.c-on-base.b--muted-4.hover-b--muted-3.t-body.pl5")
        search_box.clear()
        search_box.send_keys(codigo_barras)
        time.sleep(1)
        
        # Enviar la búsqueda presionando Enter
        search_box.send_keys(Keys.RETURN)

    # Esperar a que se cargue la página de resultados
    driver.implicitly_wait(5)

    try:
        # Esperar a que se cargue el elemento del producto
        product_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body"))
        )

        # Extraer el texto del elemento del producto
        product_text = product_element.text

        # Imprimir el texto del producto
        print("Texto del producto:", product_text)

        # Esperar a que se cargue el precio del producto 
        # Selling price es precio actual con descuento incluido si lo tiene
        price_element = WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.valtech-carrefourar-product-price-0-x-sellingPrice"))
        )

        try:
            # List price es precio sin descuento 
            old_price_element = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.valtech-carrefourar-product-price-0-x-listPrice"))
            )
            
            # Extraer el precio completo utilizando el atributo textContent
            price = price_element.get_attribute("textContent")
            old_price = old_price_element.get_attribute("textContent")
            
            # Imprimir el precio del producto
            print("Precio del producto actual:", price)
            print("Precio del producto de lista:", old_price)
            
        except TimeoutException:
            # Si no se encuentra el precio sin descuento, imprimir solo el precio actual
            price = price_element.get_attribute("textContent")
            print("Precio del producto actual:", price)
            print("No tiene descuento")
        
    except TimeoutException:
        print("Producto no encontrado")

    # Cerrar el navegador
    driver.quit()



def leer_codigos_desde_excel(archivo_excel):
    try:
        # Lee el archivo Excel y obtiene los códigos de barras de la primera columna
        df = pd.read_excel(archivo_excel, header=None)  # Sin encabezados
        codigos = df.iloc[:, 0].tolist()  # Toma solo la primera columna
        return codigos
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        return []


archivo_excel = "codigos.xlsx"  # Ruta de tu archivo Excel
codigos_barra = leer_codigos_desde_excel(archivo_excel)


print("---------- Carrefour ----------")
for codigo in codigos_barra:
    print(f"Buscando productos para el código de barras: {codigo}")
    buscador_carrefour(codigo)
    
    print("\n")
