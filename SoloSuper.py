import pandas as pd
import customtkinter as ctk
from tkinter import Tk, Button, Label, filedialog, Frame, N, S, E, W
from tkinter.ttk import Style
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import concurrent.futures 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


# Definición de los sitios de búsqueda y sus funciones
sitios_busqueda = {
    "Carrefour": False,
    "Disco": False,
    "Libertad": False
}

""" def buscador_superMami(codigo_barras):
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
 """

def buscador_disco(codigo_barra):
    
    # Crear un objeto de perfil de Firefox
    options = Options()
    options.add_argument("--headless") 
    
    profile_path = "C:/Users/Administrador/AppData/Roaming/Mozilla/Firefox/Profiles/xz3nl977.default-release"
    options.profile = webdriver.FirefoxProfile(profile_path)
    
    # Iniciar WebDriver con el perfil existente
    driver = webdriver.Firefox(options=options)

    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}

    try:
        # Navegar a la página de Disco con el código de barras
        url = f"https://www.disco.com.ar/{codigo_barra}?_q={codigo_barra}&map=ft"
        driver.get(url)

        time.sleep(7)  # Esperar unos segundos para que los precios se actualicen

        # Extraer el precio actual
        try:
            precio_actual_element = driver.find_element(By.ID, "priceContainer")
            precio_actual = precio_actual_element.text.strip()
            print(f"Precio actual: {precio_actual}")
        except Exception as e:
            print(f"No se encontró el precio actual: {e}")
            precio_actual = "Not found"

        # Extraer el precio anterior
        try:
            precio_anterior_element = driver.find_element(By.CSS_SELECTOR, "div.discoargentina-store-theme-2t-mVsKNpKjmCAEM_AMCQH")
            precio_anterior = precio_anterior_element.text.strip()
        except Exception as e:
            print(f"No se encontró el precio anterior: {e}")
            precio_anterior = precio_actual  # Usar el precio actual como fallback

        salida = {"producto": "Producto", "precio_actual": precio_actual, "precio_anterior": precio_anterior}
    
    except Exception as e:
        print(f"Error en buscador_disco: {e}")
        salida = {"producto": "Producto", "precio_actual": "error", "precio_anterior": "error"}

    finally:
        driver.quit()

    return salida


def buscador_libertad(codigo_barras):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}

    try:
        driver.get("https://www.hiperlibertad.com.ar/")

        # Manejar modal si es necesario
        try:
            modal_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.hiperlibertad-store-selector-1-x-popupModal.flex.w-100.vh-100.fixed.top-0.left-0.justify-center.items-center"))
            )
            driver.execute_script("arguments[0].style.display = 'none';", modal_element)
        except TimeoutException:
            pass  # No se encontró el modal, continuar

        # Buscar el cuadro de búsqueda
        search_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.vtex-styleguide-9-x-input.ma0.border-box.vtex-styleguide-9-x-hideDecorators.vtex-styleguide-9-x-noAppearance.br2.br-0.br--left.w-100.bn.outline-0.bg-base.c-on-base.b--muted-4.hover-b--muted-3.t-body.pl5"))
        )

        search_box.clear()
        search_box.send_keys(codigo_barras)
        time.sleep(2)
        search_box.send_keys(Keys.RETURN)

        # Esperar a que se cargue la página de resultados
        driver.implicitly_wait(4)

        # Verificar si se encontraron resultados
        results_elements = driver.find_elements(By.CSS_SELECTOR, "div.vtex-search-result-3-x-notFound--layout")
        if results_elements:
            # No se encontraron resultados
            salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}
        else:
            # Esperar a que se cargue el precio del producto
            try:
                price_element = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.vtex-product-price-1-x-sellingPriceValue"))
                )
                price = price_element.get_attribute("textContent").strip()

                try:
                    old_price_element = WebDriverWait(driver, 3).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.vtex-product-price-1-x-listPrice"))
                    )
                    old_price = old_price_element.get_attribute("textContent").strip()
                except TimeoutException:
                    old_price = price  # Si no hay precio anterior, usar el mismo que el actual

                salida = {"producto": "Producto", "precio_actual": price, "precio_anterior": old_price}
            except (TimeoutException, NoSuchElementException):
                salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}

    except Exception as e:
        print(f"Error en buscador_libertad: {e}")
    finally:
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
import concurrent.futures

def procesar_archivo(archivo_excel):
    codigos_barra, nombres_productos = leer_codigos_desde_excel(archivo_excel)
    
    # Crear un DataFrame vacío
    df_resultados = pd.DataFrame(columns=["Código de Barras", "Producto", "Sitio", "Precio", "Precio s/ Dto"])
    
    tiempo_inicio = time.time()

    # Función para buscar en todos los sitios simultáneamente
    def buscar_en_sitios(codigo, nombre_producto):
        resultados = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            sitios = {
                "Carrefour": executor.submit(buscador_carrefour, codigo),
                "Disco": executor.submit(buscador_disco, codigo),
                "Libertad": executor.submit(buscador_libertad, codigo)
            }
            
            for sitio, future in sitios.items():
                resultado = future.result()
                if resultado["producto"]:
                    resultados.append([codigo, nombre_producto, sitio, resultado["precio_actual"], resultado["precio_anterior"]])
        return resultados

    # Procesar cada código de barras
    for i, (codigo, nombre_producto) in enumerate(zip(codigos_barra, nombres_productos), 1):
        print(f"Buscando productos para el código de barras: {codigo}")
        
        # Buscar en todos los sitios en paralelo
        resultados = buscar_en_sitios(codigo, nombre_producto)
        
        # Agregar los resultados al DataFrame
        for resultado in resultados:
            df_resultados = pd.concat([df_resultados, pd.DataFrame([resultado], columns=df_resultados.columns)], ignore_index=True)

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
        "Disco Precio", "Disco Precio s/ Dto", 
        "Libertad Precio", "Libertad Precio s/ Dto"
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


# Configurar la ventana principal con customtkinter
root = ctk.CTk()  # Utilizamos CTk en lugar de Tk
root.title("Cargador de Archivos Excel")
root.geometry("400x150")
root.resizable(False, False)

# Crear un marco para centrar contenido
frame = ctk.CTkFrame(root)
frame.pack(padx=0, pady=0, fill="both", expand=True)

# Etiqueta
label = ctk.CTkLabel(frame, text="Seleccione el archivo Excel con los códigos de barras", font=ctk.CTkFont(size=14))
label.pack(pady=20)

# Botón para cargar archivo
boton = ctk.CTkButton(frame, text="Cargar archivo", command=seleccionar_archivo)
boton.pack(pady=10)

# Ejecutar la ventana principal
root.mainloop()