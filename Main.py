import pandas as pd
from Carrefour import buscador_carrefour
from Farmacity import buscador_farmacity
from Libertad import buscador_libertad
from Lider import buscador_lider
from SuperMami import buscador_superMami

def leer_codigos_desde_excel(archivo_excel):
    try:
        df = pd.read_excel(archivo_excel, header=None)
        codigos = df.iloc[:, 0].tolist()
        nombres_productos = df.iloc[:, 1].tolist()  # Leer la segunda columna con los nombres de los productos
        return codigos, nombres_productos
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        return [], []

archivo_excel = "codigos1.xlsx"
codigos_barra, nombres_productos = leer_codigos_desde_excel(archivo_excel)

# Crear un DataFrame vacío
df_resultados = pd.DataFrame(columns=["Código de Barras", "Producto", "Sitio", "Precio Actual", "Precio Anterior"])

for codigo, nombre_producto in zip(codigos_barra, nombres_productos):
    print("\n")
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
    "Super Mami Precio", "Super Mami Precio s/ Dto"
]

# Reordenar las columnas
df_resultados_pivot = df_resultados_pivot[column_order]

# Mostrar el DataFrame con los resultados
print(df_resultados_pivot)

# Guardar el DataFrame en un archivo Excel
df_resultados_pivot.to_excel("resultados_busqueda.xlsx", index=False)
