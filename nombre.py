
import csv
import random

COSTE_PRUEBA = 100000
PRECIO_CONTRATACION = 6400


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


def greedyAlgorith(presupuesto, lista_greedy_ordenado, coste_total=0, riesgo=0):
    lista_optimizada = []
    roles_seleccionados = set()
    
    candidatos = lista_greedy_ordenado.copy()

    while candidatos and coste_total < presupuesto:
        elemento = candidatos.pop(0)
        
        if elemento["role_id"] not in roles_seleccionados:
            if coste_total + elemento["cost"] <= presupuesto:
                
                coste_total += elemento["cost"]
                riesgo += elemento["risk_impact"]
                
                lista_optimizada.append(elemento)

                roles_seleccionados.add(elemento["role_id"])
                
    return lista_optimizada

lista_csv = cargarDatosCSV("roles_costs_with_month_column.csv")
lista_greedy = cargarDatosParaGreedy(lista_csv)
lista_greedy_ordenada = sorted(lista_greedy, key=lambda x: x["ratio"], reverse=True)


listado_optimo_1 = greedyAlgorith(COSTE_PRUEBA,lista_greedy_ordenada)

printedo = [item["risk_impact"] for item in listado_optimo_1]
print(sum(printedo))
printedo = [item["cost"] for item in listado_optimo_1]
print(sum(printedo))
printedo = [item["role_id"] for item in listado_optimo_1]
print(printedo)




