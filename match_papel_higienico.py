import pandas as pd
from tqdm import tqdm
import difflib
from config import *
def get_categoria(diccionario):
    max_value = max(diccionario, key=diccionario.get)
    return max_value
def match_palabras(descripcion_factura, maestro):
    max_ratio = 0
    producto_max_ratio =""
    for i in maestro:
        if "RINDEMAX" in descripcion_factura:
            print()
        ratio = difflib.SequenceMatcher(None, i, descripcion_factura).ratio()
        if ratio > 0.45 and ratio>max_ratio:
            max_ratio = ratio
            producto_max_ratio = i
        if i in descripcion_factura.split() :
            return i
    if max_ratio != 0:
        return producto_max_ratio

"""
for index_facturas, row_facturas in tqdm(facturas.iterrows(), total= facturas.shape[0]):
    try:
        descripcion_facturas= row_facturas["descripcion"]
        #df[df['ids'].str.contains("ball")]
        for palabra_factura in descripcion_facturas.split(" "):
            if not str(palabra_factura).isnumeric() and len(str(palabra_factura)) > 4:
                categorias_filtradas = categorias[categorias["DescripcionLargaProducto"].str.contains(palabra_factura)]
                for index_categorias, row_categorias in categorias_filtradas.iterrows():
                    descripcion_categorias = row_categorias["DescripcionLargaProducto"]
                    categoria_categorias = row_categorias["SubCategoria"]
                    if palabra_factura in str(descripcion_categorias):
                        if  not palabra_factura in contador_palabras_categorias:
                            contador_palabras_categorias[palabra_factura] = {}
                            contador_palabras_categorias[palabra_factura][categoria_categorias] = 1
                        else:
                            if  not categoria_categorias in contador_palabras_categorias[palabra_factura]:
                                contador_palabras_categorias[palabra_factura][categoria_categorias] = 1
                            else:
                                contador_palabras_categorias[palabra_factura][categoria_categorias] =  contador_palabras_categorias[palabra_factura][categoria_categorias] +1
    except Exception as e:
        print (e)

with open("sample.json", "w") as outfile:
    json.dump(contador_palabras_categorias, outfile)
"""

"""
with open('sample.json') as f:
    data = f.read()

print("Data type before reconstruction : ", type(data))

# reconstructing the data as a dictionary
contador_palabras_categorias = json.loads(data)
categorias_encontradas = []

for index_facturas, row_facturas in tqdm(facturas.iterrows(), total= facturas.shape[0]):
    descripcion_facturas = row_facturas["descripcion"]
    dict_final = {}
    for palabra_factura in descripcion_facturas.split(" "):
        if not str(palabra_factura).isnumeric() and len(str(palabra_factura)) > 4:
            categoria_palabra = get_categoria(contador_palabras_categorias[palabra_factura])
            if not categoria_palabra in dict_final:
                dict_final[categoria_palabra] = 1
            else:
                dict_final[categoria_palabra] = dict_final[categoria_palabra] +1
    categorias_encontradas.append(get_categoria(dict_final))
facturas["Categoria"]
print ()
"""
def procesar(df):
    categorias = pd.read_csv("Categorias.csv", sep=";")
    categorias = categorias[~pd.isna(categorias["SubCategoria"])]
    categorias = categorias[~pd.isna(categorias["DescripcionLargaProducto"])]
    precios = pd.read_excel("Precio promedio Papel higienico septiembre-octubre 2022.xlsx", index_col=None)
    facturas = df
    contador_palabras_categorias={}
    columna_categorias = []
    subcategorias=[]
    words_list = categorias["DescripcionLargaProducto"].unique().tolist()
    words_list_descripciones_proyecto_ph = precios["Descripciones PH Familia"].unique().tolist()
    words_list_descripciones_maestro_precios = precios["DescripcionLargaProducto (copia)"].unique().tolist()
    math_maestro_precios_descripciones = []
    math_maestro_precios_codigos = []
    for index_facturas, row_facturas in tqdm(facturas.iterrows(), total= facturas.shape[0]):
        #try:

        descripcion_facturas = row_facturas["descripcion"]
        #comparacion_maestro_tr = difflib.get_close_matches(descripcion_facturas,words_list, cutoff = 0.5)
        #comparacion_maestro_papel_higienico_factura = difflib.get_close_matches(str(descripcion_facturas),words_list_descripciones_proyecto_ph)
        descripcion_match_calculada = match_palabras(str(descripcion_facturas), words_list_descripciones_proyecto_ph)
        #comparacion_maestro_papel_higienico_maestro_precios = difflib.get_close_matches(descripcion_facturas,words_list_descripciones_maestro_precios, cutoff = 0.5)
        """
        #a = difflib.get_close_matches(descripcion_facturas, words_list, cutoff=0.05)
        conteo = dict((x,comparacion_maestro_tr.count(x)) for x in set(comparacion_maestro_tr))
        max_value = comparacion_maestro_tr[0]
        precio_factura = row_facturas["precio unit"]
        cantidad_factura = row_facturas["cantidad"]
        codigo_barras = categorias[categorias["DescripcionLargaProducto"] == max_value]["CodigoDeBarras"].tolist()[0]
        categoria = categorias[categorias["DescripcionLargaProducto"] == max_value]["SubCategoria"].tolist()[0]
        subcategoria = categorias[categorias["DescripcionLargaProducto"] == max_value]["Categoria"].tolist()[0]
        subcategorias.append(subcategoria)
        columna_categorias.append(categoria)
        #['PAPEL HIGIENICO SCOTT CUIDADO COMPLETO X 4 UN', 'PAPEL HIGIENICO SCOTT CUIDADO COMPLETO X 4 UN', 'PAPEL HIGIENICO SCOTT CUIDADO COMPLETO X 12 UN']
        print(f"{descripcion_facturas} --> {max_value} --> {categoria} --> {subcategoria}")
    except Exception as e:
        subcategorias.append("No se parece a nada")
        columna_categorias.append("No se parece a nada")
        """
        try:
            if descripcion_match_calculada != None:
                # cb_match = precios[precios["TBLvProductos_CodigoDeBarras"] == codigo_barras]["Precio promedio de venta"].tolist()[0]
                cb_match = precios[precios["Descripciones PH Familia"] == descripcion_match_calculada][
                    "TBLvProductos_CodigoDeBarras"].tolist()[0]
                descripcion_match = precios[precios["Descripciones PH Familia"] == descripcion_match_calculada][
                    "DescripcionLargaProducto (copia)"].tolist()[0]
                math_maestro_precios_descripciones.append(descripcion_match)
                math_maestro_precios_codigos.append(cb_match)
            else:
                math_maestro_precios_descripciones.append("No es de papel higienico")
                math_maestro_precios_codigos.append("No es de papel higienico")
        except Exception as e:
            math_maestro_precios_descripciones.append("No es de papel higienico")
            math_maestro_precios_codigos.append("No es de papel higienico")
    #facturas["SubCategoria"] = columna_categorias
    facturas["descripcionTR"] = math_maestro_precios_descripciones
    facturas["cbTR"] = math_maestro_precios_codigos
    #facturas.to_csv("facturas_modificado_v6.csv", sep =";")
    facturas.to_excel(f"Salida/{version_lectura}/match_PH.xlsx")
    return facturas

def limpieza_final(df):
    data_original = df
    data_revisada = pd.read_excel("09-02-2023Match_Solr_New_Model_textos_procesados_match_Tiendas_TR_nuevo_ph_v2.xlsx",
                                  index_col=None)
    data_unida = data_original.merge(data_revisada, on="descripcion", how="left")

    data_unida.loc[data_unida["Tipo"] == 1, "Descricion_tr_nuevo_match_ph"] = "No Encontrado"
    data_unida.loc[data_unida["Tipo"] == 1, "Codigos_barra_tr_nuevo_match_ph"] = "No Encontrado"
    data_unida.loc[data_unida["Tipo"] == 1, "Promociones_tr_nuevo_match_ph"] = "No Encontrado"

    data_eliminada = data_unida[data_unida["Tipo"] != 2]

    data_eliminada.loc[data_unida["Tipo"] == 3, "Descricion_tr_nuevo_match_ph"] = "Es de PH pero no identifico cual"
    data_eliminada.loc[data_unida["Tipo"] == 3, "Codigos_barra_tr_nuevo_match_ph"] = "Es de PH pero no identifico cual"
    data_eliminada.loc[data_unida["Tipo"] == 3, "Promociones_tr_nuevo_match_ph"] = "Es de PH pero no identifico cual"

    data_eliminada.to_excel(f"Salida/{version_lectura}/Data_final.xlsx", index=None)

    return data_eliminada