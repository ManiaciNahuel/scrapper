import pandas as pd
from tkinter import Tk, Button, Label, filedialog, Frame, N, S, E, W
from tkinter.ttk import Progressbar, Style
from Carrefour import buscador_carrefour
from Farmacity import buscador_farmacity
from Ferniplast import buscador_ferniplast
from Libertad import buscador_libertad
from Lider import buscador_lider
from SuperMami import buscador_superMami
import time

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