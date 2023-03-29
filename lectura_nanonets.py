import pandas as pd
import requests
import json
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
                try:
                    contador+=1
                    print (f"PORCENTAJE = {(contador*100)/3}")
                    if not "Imágenes_Feas" in path:
                        img  = os.path.join(path, name)
                        valor_random = random.rand()
                        if valor_random <= ratio_lectura:
                            numero_muestras +=1
                            data = {'file': open(img, 'rb')}
                            response = requests.post(url_nanonets, auth=requests.auth.HTTPBasicAuth(api_key, ''), files=data)
                            # with open('response_test.json', 'r') as file:
                            #     data = json.load(file)
                            #
                            # print(data)

                            data = json.loads(response.text)
                            ruta = f"Salida/{version_lectura}/json"
                            if not os.path.isdir(ruta):
                                # if the demo_folder2 directory is
                                # not present then create it.
                                os.makedirs(ruta)
                            with open(f'{ruta}/{name.split(".")[0]}.json', 'w') as convert_file:
                                convert_file.write(json.dumps(data))


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

                            len_list = [len(a) for a in tabla.values()]
                            len_mode = max(set(len_list), key=len_list.count)
                            columnas_a_borrar =[]
                            for key in tabla:
                                if len(tabla[key]) != len_mode:
                                    columnas_a_borrar.append(key)
                            for columna in columnas_a_borrar:
                                tabla.pop(columna)
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

                            if 'BARRANQUILLA' in str(img).upper():
                                df["ciudad_verdadera"] = 'BARRANQUILLA'
                            elif 'BOGOTA' in str(img).upper():
                                df["ciudad_verdadera"] = 'BOGOTA'
                            elif 'CALI' in str(img).upper():
                                df["ciudad_verdadera"] = 'CALI'
                            elif 'MEDELLIN' in str(img).upper():
                                df["ciudad_verdadera"] = 'MEDELLIN'
                            else:
                                df["ciudad_verdadera"] = 'NO EXTRAIDA'
                            df["ruta_factura"] = img
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
                                            print ()
                                            temp_list = [None] * df_final.shape[0]
                                            temp_list.extend(df[columna].tolist())
                                            df_auxiliar[columna] = temp_list
                                    for columna in df_final.columns:
                                        if  not columna in df.columns:
                                            df_auxiliar[columna] = df_final[columna]
                                    df_final = df_auxiliar
                                    #columnas = df_final.columns.tolist()
                                    #df_final = pd.DataFrame(np.concatenate((df_final.values, df.values), axis=0))
                                    #df_final.columns = columnas



                            facturas_buenas_muestra += 1
                except Exception as e:
                    facturas_malas_muestra += 1
                    print(F"ERRRORR CON IMAGEN {img} = {e}")


        except Exception as e:
            facturas_malas_muestra +=1
            print (F"ERRRORR CON IMAGEN {img} = {e}")

    print (f"numero de muestras = {numero_muestras} \n "
           f"Facturas buenas de la muestra = {facturas_buenas_muestra} \n"
           f"Facturas malas de la muestra = {facturas_malas_muestra}")
    # checking if the directory demo_folder2
    # exist or not.
    if not os.path.isdir(f"Salida/{version_lectura}"):
        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(f"Salida/{version_lectura}")
    df_final.to_excel(f"Salida/{version_lectura}/lectura_nanonets.xlsx", index=None)
    return df_final
