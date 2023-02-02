import pandas as pd
import requests
import json
import os
from numpy import random
from tqdm import tqdm
from config import *

def procesar():
    df_final = None
    valor_random = 0
    numero_muestras = 0
    facturas_buenas_muestra = 0
    facturas_malas_muestra = 0
    contador = 0
    for path, subdirs, files in tqdm(os.walk(ruta_imagenes)):
        try:
            for name in files:
                contador+=1
                print (f"PORCENTAJE = {(contador*100)/2906}")
                if not "Imágenes_Feas" in path:
                    img  = os.path.join(path, name)
                    valor_random = random.rand()
                    if valor_random < ratio_lectura:
                        numero_muestras +=1
                        data = {'file': open(img, 'rb')}
                        response = requests.post(url_nanonets, auth=requests.auth.HTTPBasicAuth(api_key, ''), files=data)
                        # with open('response_test.json', 'r') as file:
                        #     data = json.load(file)
                        #
                        # print(data)
                        data = json.loads(response.text)
                        resultados = data["result"][0]['prediction']
                        print (resultados)
                        cabeceras = {}
                        tabla = {}
                        for key in resultados:
                            if key["label"] != "table":
                                cabeceras[key["label"]] = key["ocr_text"]
                            else:
                                celdas = key["cells"]
                                for celda in celdas:
                                    if not celda["label"]  in tabla:
                                        tabla[celda["label"]] = []
                                    tabla[celda["label"]].append(celda["text"])

                        df = pd.DataFrame(tabla)
                        # longitud_mas_comun = 0
                        # longitudes =[]
                        # longitudes = [len(cabeceras[x]) for x in cabeceras.keys()]
                        # vals, counts = np.unique(longitudes, return_counts=True)
                        # longitud_mas_comun = vals[counts == np.max(counts)]
                        for cabecera in cabeceras:
                            # if len(cabeceras[cabecera]) == longitud_mas_comun:
                            #longitudes = len(cabeceras[cabecera])
                            df[cabecera] = cabeceras[cabecera]
                        df["ruta_factura"] = img
                        facturas_buenas_muestra +=1
                        if df_final is None:
                            df_final = df.infer_objects()
                        else:
                                df_auxiliar = pd.DataFrame()
                                for columna in df.columns:
                                    if columna in df_final.columns.tolist():
                                        aux = df_final[columna].tolist().copy()
                                        aux.extend(df[columna].tolist())
                                        df_auxiliar[columna] = aux
                                    else:
                                        df_auxiliar[columna] = df[columna]
                                for columna in df_final.columns:
                                    if  not columna in df.columns:
                                        df_auxiliar[columna] = df_final[columna]
                                df_final = df_auxiliar
                                #columnas = df_final.columns.tolist()
                                #df_final = pd.DataFrame(np.concatenate((df_final.values, df.values), axis=0))
                                #df_final.columns = columnas
        except Exception as e:
            facturas_malas_muestra +=1
            print (F"ERRRORR CON IMAGEN {img} = {e}")

    print (f"numero de muestras = {numero_muestras} \n "
           f"Facturas buenas de la muestra = {facturas_buenas_muestra}"
           f"Facturas malas de la muestra = {facturas_malas_muestra}")
    # checking if the directory demo_folder2
    # exist or not.
    if not os.path.isdir(f"Salida/{version_lectura}"):
        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(f"Salida/{version_lectura}")
    df_final.to_excel(f"Salida/{version_lectura}/lectura_nanonets.xlsx", index=None)
    return df_final
