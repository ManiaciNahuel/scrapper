import pandas as pd
from tkinter import Tk, Button, Label, filedialog, Frame, N, S, E, W
from tkinter.ttk import Style
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
        boton = WebDriverWait(driver, 4).until(
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
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.precio-unidad"))
            )
            # Encontrar los elementos que contienen los precios del producto buscado
            precios = driver.find_elements(By.CSS_SELECTOR, "div.precio-unidad span")
            if len(precios) >= 2:
                precio_actual = precios[0].text.strip()
                precio_anterior = precios[1].text.strip()
                salida = {"producto": "Producto", "precio_actual": precio_actual, "precio_anterior": precio_anterior}
            elif len(precios) >= 1:
                precio_actual = precios[0].text.strip()
                # El producto no tiene descuentos
                salida = {"producto": "Producto", "precio_actual": precio_actual, "precio_anterior": precio_actual}
            else:
                # No se encontraron precios para el producto buscado
                pass
        except:
            # Producto no encontrado
            pass
    except Exception as e:
        # Error al conectar con la página web
        # Asegúrate de tener conexión a Internet y que la URL sea correcta.
        print(f"Error en buscador_superMami: {e}")
        # Continuar con el próximo buscador
        driver.quit()
        return {"producto": "Producto", "precio_actual": "URL error", "precio_anterior": "URL error"}

    driver.quit()
    return salida

def buscador_lider(codigo_barra):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}

    try:
        url = f"https://farmaciaslider.com.ar/busqueda?controller=search&s={codigo_barra}"
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
                    else:
                        salida = {"producto": "Producto", "precio_actual": precio_actual, "precio_anterior": precio_actual}
    except Exception as e:
        print(f"Error en buscador_lider: {e}")
        driver.quit()
        return {"producto": "Producto", "precio_actual": "error", "precio_anterior": "error"}

    driver.quit()
    return salida


def buscador_libertad(codigo_barras):
    # Options con --headless es para que no se vea la pestaña abierta
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}

    # Navegar a la página de Hiper Libertad
    driver.get("https://www.hiperlibertad.com.ar/")
    modal_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.hiperlibertad-store-selector-1-x-popupModal.flex.w-100.vh-100.fixed.top-0.left-0.justify-center.items-center"))
    )
    driver.execute_script("arguments[0].style.display = 'none';", modal_element)

    # Esperar a que el elemento de búsqueda esté presente y visible
    search_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.vtex-styleguide-9-x-input.ma0.border-box.vtex-styleguide-9-x-hideDecorators.vtex-styleguide-9-x-noAppearance.br2.br-0.br--left.w-100.bn.outline-0.bg-base.c-on-base.b--muted-4.hover-b--muted-3.t-body.pl5"))
    )

    try:
        search_box.clear()
        # Ingresar el código de barras
        search_box.send_keys(codigo_barras)
        # Pequeña pausa antes de enviar la búsqueda
        time.sleep(2)
        # Enviar la búsqueda presionando Enter
        search_box.send_keys(Keys.RETURN)
    except TimeoutException:
        print("No tiene descuento")
    except StaleElementReferenceException:
        # El elemento de búsqueda se ha vuelto'stale', volviendo a encontrarlo
        search_box = driver.find_element(By.CSS_SELECTOR, "input.vtex-styleguide-9-x-input.ma0.border-box.vtex-styleguide-9-x-hideDecorators.vtex-styleguide-9-x-noAppearance.br2.br-0.br--left.w-100.bn.outline-0.bg-base.c-on-base.b--muted-4.hover-b--muted-3.t-body.pl5")
        search_box.clear()
        search_box.send_keys(codigo_barras)
        time.sleep(2)
        # Enviar la búsqueda presionando Enter
        search_box.send_keys(Keys.RETURN)

    # Esperar a que se cargue la página de resultados
    driver.implicitly_wait(4)

    try:
        modal_element = WebDriverWait(driver, 4).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.hiperlibertad-store-selector-1-x-popupModal.flex.w-100.vh-100.fixed.top-0.left-0.justify-center.items-center"))
        )
        driver.execute_script("arguments[0].style.display = 'none';", modal_element)

        # Esperar a que se cargue el precio del producto
        # Selling price es precio actual con descuento incluido si lo tiene
        price_element = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.vtex-product-price-1-x-sellingPriceValue"))
        )

        try:
            # List price es precio sin descuento
            old_price_element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.vtex-product-price-1-x-listPrice"))
            )
            # Extraer el precio completo utilizando el atributo textContent
            price = price_element.get_attribute("textContent")
            old_price = old_price_element.get_attribute("textContent")
            salida = {"producto": "Producto", "precio_actual": price, "precio_anterior": old_price}
        except TimeoutException:
            # Si no se encuentra el precio sin descuento, imprimir solo el precio actual
            price = price_element.get_attribute("textContent")
            salida = {"producto": "Producto", "precio_actual": price, "precio_anterior": price}
    
    except Exception as e:
        print(f"Error en buscador_libertad: {e}")
        driver.quit()
        return {"producto": "Producto", "precio_actual": "error", "precio_anterior": "error"}

    driver.quit()
    return salida
 
  
def buscador_farmacity(codigo_barra):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}

    try:
        # Navegar a la página de Farmacity
        driver.get("https://www.farmacity.com/")
        campo_busqueda = WebDriverWait(driver, 4).until(
            EC.visibility_of_element_located((By.ID, "downshift-0-input"))
        )
        campo_busqueda.click()
        campo_busqueda.send_keys(codigo_barra)
        campo_busqueda.send_keys(Keys.RETURN)
        time.sleep(4)

        try:
            not_found_element = driver.find_elements(By.CLASS_NAME, "farmacityar-store-components-1-x-notFoundText")
            no_stock_element = driver.find_elements(By.CLASS_NAME, "farmacityar-store-components-1-x-no_stock")

            # Esperar a que se cargue la página de resultados
            if not_found_element:
                # Producto no encontrado
                pass
            elif no_stock_element:
                # Producto encontrado pero sin stock disponible
                pass
            else:
                time.sleep(2)
                precio_actual = WebDriverWait(driver, 4).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.vtex-product-price-1-x-sellingPriceValue"))
                )
                precio_completo = precio_actual.text

                # Verificar si hay un precio sin descuento
                precio_lista_element = driver.find_elements(By.CSS_SELECTOR, "span.vtex-product-price-1-x-listPriceValue.strike")
                if precio_lista_element:
                    precio_lista = precio_lista_element[0].text
                    salida = {"producto": "Producto", "precio_actual": precio_completo, "precio_anterior": precio_lista}
                else:
                    # No hay precio con descuento disponible
                    salida = {"producto": "Producto", "precio_actual": precio_completo, "precio_anterior": precio_completo}
        except TimeoutException:
            pass
    except Exception as e:
        # Error al conectar con la página web
        # Asegúrate de tener conexión a Internet y que la URL sea correcta.
        print(f"Error en buscador_farmacity: {e}")
        driver.quit()
        return {"producto": "Producto", "precio_actual": "error", "precio_anterior": "error"}

    driver.quit()
    return salida
    

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
        campo_busqueda.click()
        campo_busqueda.send_keys(codigo_barra)
        campo_busqueda.send_keys(Keys.RETURN)
        time.sleep(4)

        try:
            not_found_element = driver.find_elements(By.CSS_SELECTOR, ".vtex-rich-text-0-x-container.vtex-rich-text-0-x-container--not-found.flex.tl.items-start.justify-start.t-body.c-on-base")

            # Esperar a que se cargue la página de resultados
            if not_found_element:
                # Producto no encontrado
                pass
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
                else:
                    # No hay precio con descuento disponible
                    salida = {"producto": "Producto", "precio_actual": precio_completo, "precio_anterior": precio_completo}
        except TimeoutException:
            pass
    except Exception as e:
        # Error al conectar con la página web
        # Asegúrate de tener conexión a Internet y que la URL sea correcta.
        print(f"Error en buscador_ferniplast: {e}")
        driver.quit()
        return {"producto": "Producto", "precio_actual": "error", "precio_anterior": "error"}

    driver.quit()
    return salida

def buscador_carrefour(codigo_barras):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}
    
    try:
        driver.get("https://www.carrefour.com.ar/")
        time.sleep(3)
        
        search_box = WebDriverWait(driver, 4).until(
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
            time.sleep(4)

        driver.implicitly_wait(2)

        try:
            price_element = WebDriverWait(driver, 4).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.valtech-carrefourar-product-price-0-x-sellingPrice"))
            )

            try:
                old_price_element = WebDriverWait(driver, 4).until(
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
            pass
                
    except Exception as e:
        # Error al conectar con la página web
        # Asegúrate de tener conexión a Internet y que la URL sea correcta.
        print(f"Error en buscador_carrefour: {e}")
        driver.quit()
        return {"producto": "Producto", "precio_actual": "error", "precio_anterior": "error"}

    driver.quit()
    return salida
    

def leer_codigos_desde_excel(archivo_excel):
    try:
        df = pd.read_excel(archivo_excel, header=None)
        codigos = df.iloc[:, 0].tolist()
        nombres_productos = df.iloc[:, 1].tolist()  # Leer la segunda columna con los nombres de los productos
        return codigos, nombres_productos
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        return [], []

def seleccionar_archivo():
    archivo_excel = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if archivo_excel:
        procesar_archivo(archivo_excel)

def procesar_archivo(archivo_excel):
    codigos_barra, nombres_productos = leer_codigos_desde_excel(archivo_excel)
    
    # Crear un DataFrame vacío
    df_resultados = pd.DataFrame(columns=["Código de Barras", "Producto", "Sitio", "Precio", "Precio s/ Dto"])
    
    tiempo_inicio = time.time()
    
    for i, (codigo, nombre_producto) in enumerate(zip(codigos_barra, nombres_productos), 1):
        print(f"Buscando productos para el código de barras: {codigo}")
        
        # Buscadores
        resultado_carrefour = buscador_carrefour(codigo)
        if resultado_carrefour["producto"]:
            df_resultados = pd.concat([df_resultados, pd.DataFrame([[codigo, nombre_producto, "Carrefour", resultado_carrefour["precio_actual"], resultado_carrefour["precio_anterior"]]], columns=df_resultados.columns)], ignore_index=True)
        
        resultado_libertad = buscador_libertad(codigo)
        if resultado_libertad["producto"]:
            df_resultados = pd.concat([df_resultados, pd.DataFrame([[codigo, nombre_producto, "Libertad", resultado_libertad["precio_actual"], resultado_libertad["precio_anterior"]]], columns=df_resultados.columns)], ignore_index=True)
        
        resultado_superMami = buscador_superMami(codigo)
        if resultado_superMami["producto"]:
            df_resultados = pd.concat([df_resultados, pd.DataFrame([[codigo, nombre_producto, "Super Mami", resultado_superMami["precio_actual"], resultado_superMami["precio_anterior"]]], columns=df_resultados.columns)], ignore_index=True)
        
        resultado_lider = buscador_lider(codigo)
        if resultado_lider["producto"]:
            df_resultados = pd.concat([df_resultados, pd.DataFrame([[codigo, nombre_producto, "Lider", resultado_lider["precio_actual"], resultado_lider["precio_anterior"]]], columns=df_resultados.columns)], ignore_index=True)
        
        resultado_farmacity = buscador_farmacity(codigo)
        if resultado_farmacity["producto"]:
            df_resultados = pd.concat([df_resultados, pd.DataFrame([[codigo, nombre_producto, "Farmacity", resultado_farmacity["precio_actual"], resultado_farmacity["precio_anterior"]]], columns=df_resultados.columns)], ignore_index=True)

        resultado_ferniplast = buscador_ferniplast(codigo)
        if resultado_ferniplast["producto"]:
            df_resultados = pd.concat([df_resultados, pd.DataFrame([[codigo, nombre_producto, "Ferniplast", resultado_ferniplast["precio_actual"], resultado_ferniplast["precio_anterior"]]], columns=df_resultados.columns)], ignore_index=True)


    tiempo_total = time.time() - tiempo_inicio
    print(f"Tiempo total de ejecución: {tiempo_total} segundos")
    # Pivotear el DataFrame para tener una fila por código de barras
    df_resultados_pivot = df_resultados.pivot(index=["Código de Barras", "Producto"], columns="Sitio", values=["Precio", "Precio s/ Dto"])

    # Renombrar las columnas con el nombre del comercio y el tipo de precio
    df_resultados_pivot.columns = [f"{col[1]} {col[0]}" if col[1] != '' else col[0] for col in df_resultados_pivot.columns]

    # Resetear el índice para que "Código de Barras" y "Producto" sean columnas normales
    df_resultados_pivot.reset_index(inplace=True)

    # Especificar el orden deseado de las columnas
    column_order = [
        "Código de Barras", "Producto", 
        "Carrefour Precio", "Carrefour Precio s/ Dto", 
        "Farmacity Precio", "Farmacity Precio s/ Dto", 
        "Libertad Precio", "Libertad Precio s/ Dto", 
        "Lider Precio", "Lider Precio s/ Dto", 
        "Super Mami Precio", "Super Mami Precio s/ Dto",
        "Ferniplast Precio", "Ferniplast Precio s/ Dto"
    ]

    # Reordenar las columnas
    df_resultados_pivot = df_resultados_pivot[column_order]

    # Mostrar el DataFrame con los resultados
    print(df_resultados_pivot)

    # Guardar el DataFrame en un archivo Excel
    archivo_guardar = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if archivo_guardar:
        df_resultados_pivot.to_excel(archivo_guardar, index=False)
        print(f"Resultados guardados en '{archivo_guardar}'")
    
    root.quit()  # Cerrar la aplicación de Tkinter

# Configurar la ventana principal de Tkinter
root = Tk()
root.title("Cargador de Archivos Excel")
root.geometry("300x180")
root.resizable(False, False)

# Estilo
style = Style(root)
style.theme_use('clam')
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12))

# Marco para centrar contenido
frame = Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky=(N, S, E, W))

# Etiqueta
label = Label(frame, text="Seleccione el archivo Excel con los códigos de barras")
label.grid(row=0, column=0, columnspan=2, pady=20)

# Botón para cargar archivo
boton = Button(frame, text="Cargar archivo", command=seleccionar_archivo)
boton.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()