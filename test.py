from resources import es_carpeta_indexada

es_carpeta_indexada("T1 - PIZARRAS ROJAS 24.07.25")  # Debe ser True
es_carpeta_indexada("T1 - YEROMI ZAVALA 27.07.25")  # Debe ser True
es_carpeta_indexada("T2 - YEROMI ZAVALA 23.07.25")  # Debe ser True
es_carpeta_indexada("T3 - VICTOR SALLUCA 24.07.25")  # Debe ser True
es_carpeta_indexada("T0 - YEROMI ZAVALA 24.07.25")  # Debe ser False
es_carpeta_indexada("YEROMI ZAVALA 24.07.25")  # Debe ser False