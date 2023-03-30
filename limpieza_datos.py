from config import *
from tqdm import tqdm
import pandas as pd
def procesar(df):
    for contenedor in contenedores:
        for valor in contenedores[contenedor]:
            #datos_nanonets = datos_nanonets.query(f"not {contenedor}.str.contains('{valor}')", engine='python')
            if contenedor in datos_nanonets.columns:
                datos_nanonets = datos_nanonets[~datos_nanonets[contenedor].astype(str).str.upper().str.contains(valor.upper())]

    for index, row in tqdm(datos_nanonets.iterrows(), total= datos_nanonets.shape[0]):
        if ultima_factura != row["ruta_factura"]:
            ultima_factura = row["ruta_factura"]
            #datos_factura_especifica = datos_nanonets.query(f"numero_factura == '{row['numero_factura']}'")
            datos_factura_especifica = datos_nanonets[datos_nanonets["ruta_factura"].astype(str) == row['ruta_factura']]
            print()
            for index_factura, row_factura in datos_factura_especifica.iterrows():
                try:
                    borrar = True
                    for columna in columnas_tabla:
                        if columna in datos_factura_especifica.columns:
                            if not pd.isna(row_factura[columna]):
                                borrar = False
                                break
                    if borrar:
                        datos_nanonets.loc[index_factura - 1, "descripcion"] = f'{datos_nanonets.loc[index_factura - 1, "descripcion"]}{row_factura["descripcion"]}'
                        datos_nanonets.drop([index_factura], inplace= True)
                except Exception as e:
                    print (e)
    datos_nanonets = datos_nanonets[datos_nanonets["descripcion"].astype(str).str.len() > 2]

    datos_nanonets.to_excel(f"Salida/{version_lectura}/prueba_multilineaV2.xlsx", index = None)