import pandas as pd
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

sitios_busqueda = {
    "Ferniplast": False
}

def buscador_ferniplast(codigo_barra):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    salida = {"producto": "Producto", "precio_actual": 0, "precio_anterior": 0}

    try:
        # Navegar a la página de Ferniplast
        driver.get("https://www.ferniplast.com/")
        
        # Presionar ESC para cerrar el modal
        body = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        body.send_keys(Keys.ESCAPE)
        
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
        
        resultado_ferniplast = buscador_ferniplast(codigo)
        if resultado_ferniplast["producto"]:
            df_resultados = pd.concat([df_resultados, pd.DataFrame([[codigo, nombre_producto, "ferniplast", resultado_ferniplast["precio_actual"], resultado_ferniplast["precio_anterior"]]], columns=df_resultados.columns)], ignore_index=True)
        

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
        "ferniplast Precio", "ferniplast Precio s/ Dto"
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