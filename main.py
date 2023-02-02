import lectura_nanonets
import match_productos_general
import match_papel_higienico

datos_nanonets = lectura_nanonets.procesar()

datos_ph = match_papel_higienico.procesar(datos_nanonets)

datos_general = match_productos_general.procesar(datos_ph)

