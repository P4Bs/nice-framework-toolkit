
import csv
import random

COSTE_PRUEBA = 250000
PRECIO_CONTRATACION = 6400

ELEMENTOS_DE_PRUEBA = [
    {"nombre": "Laptop Pro",        "score": 95, "coste": 45},
    {"nombre": "Monitor Curvo",     "score": 50, "coste": 25},
    {"nombre": "Silla Ergonómica",  "score": 40, "coste": 20},
    {"nombre": "Teclado Mecánico",  "score": 25, "coste": 10},
    {"nombre": "Ratón Gaming",      "score": 20, "coste": 8},
    {"nombre": "Cascos Wireless",   "score": 30, "coste": 15},
    {"nombre": "Webcam 4K",         "score": 15, "coste": 12},
    {"nombre": "Micrófono USB",     "score": 28, "coste": 14},
    {"nombre": "Alfombrilla XL",    "score": 8,  "coste": 5},
    {"nombre": "Soporte Monitor",   "score": 12, "coste": 7},
    {"nombre": "Luz de Escritorio", "score": 18, "coste": 9},
    {"nombre": "Disco SSD 2TB",     "score": 45, "coste": 18},
    {"nombre": "Memoria RAM 32GB",  "score": 35, "coste": 12},
    {"nombre": "Cable HDMI 2.1",    "score": 5,  "coste": 3},
    {"nombre": "Hub USB-C",         "score": 10, "coste": 6},
    {"nombre": "Ventilador PC",     "score": 7,  "coste": 4},
    {"nombre": "Pasta Térmica",     "score": 3,  "coste": 2},
    {"nombre": "Tira LED RGB",      "score": 12, "coste": 10},
    {"nombre": "Altavoces 2.1",     "score": 22, "coste": 11},
    {"nombre": "Reposapiés",        "score": 15, "coste": 13}
]

def cargarDatosCSV(nombre_archivo):
    lista_elementos = []
    with open(nombre_archivo, mode='r') as archivo:

        lector = csv.DictReader(archivo)
        for fila in lector:
            item = {
                "role_id" : fila["role_id"],
                "training_cost" : int(fila["training_cost_usd"]),
                "outsourcing_cost" : int(fila["outsourcing_cost_usd"]),
                "bonus_cost" : int(fila["bonus_cost_usd"]),
                "time_to_hire" : float(fila["time_to_hire_months"]),
                "role_criticality" : float(fila["role_criticality"]),
                "risk_impact" : float(fila["risk_impact"]),
            }
            lista_elementos.append(item)

    return lista_elementos

def cargarDatosParaGreedy(lista_elementos):
    lista_contratados = []
    lista_estudiados = []
    lista_subcontratados = []

    for elemento in lista_elementos:

        riesgo = float(elemento["risk_impact"]) #Por el calculo de mitigación de riesgo 
        coste = elemento["bonus_cost"] + (elemento["time_to_hire"] * PRECIO_CONTRATACION)

        item_nuevo_contratado = {
            "role_id" : elemento["role_id"],
            "contrato" : "nuevo contratado",
            "cost":  coste,
            "risk_impact" : riesgo,
            "ratio" : riesgo / coste
        }

        lista_contratados.append(item_nuevo_contratado)

        coste = elemento["outsourcing_cost"]
        item_subcontrata = {
            "role_id" : elemento["role_id"],
            "contrato" : "subcontratado",
            "cost":  coste,
            "risk_impact" : riesgo,
            "ratio" : riesgo / coste
        }

        lista_subcontratados.append(item_subcontrata)
        
        coste = elemento["training_cost"]
        item_aprendido = {
            "role_id" : elemento["role_id"],
            "contrato" : "entrenado",
            "cost":  coste,
            "risk_impact" : riesgo,
            "ratio" : riesgo / coste
        } 

        lista_estudiados.append(item_aprendido)
    
    return lista_estudiados + lista_contratados + lista_subcontratados


#lista_elementos = cargarDatosCSV(csv_roles_name)
#lista_greedy = cargarDatosParaGreedy(lista_elementos)


def greedyAlgorith(presupuesto, lista_greedy_ordenado, coste_total=0, riesgo=0): #coste_total y riesgo son los valores iniciales, se usan para intentar impedir máximos locales
    lista_optimizada = []
    while(coste_total < presupuesto and lista_greedy_ordenado):
        elemento = lista_greedy_ordenado.pop(0)

        coste_total += elemento["cost"]
        riesgo += elemento["risk_impact"]
        lista_optimizada.append(elemento)
        
    
    return lista_optimizada


lista_csv = cargarDatosCSV("roles_costs_with_month_column.csv")
lista_greedy = cargarDatosParaGreedy(lista_csv)
lista_greedy_ordenada = sorted(lista_greedy, key=lambda x: x["ratio"], reverse=True)


listado_optimo_1 = greedyAlgorith(COSTE_PRUEBA,lista_greedy_ordenada)

printedo = [item["risk_impact"] for item in listado_optimo_1]
print(sum(printedo))
printedo = [item["cost"] for item in listado_optimo_1]
print(sum(printedo))



