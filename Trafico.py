# Simulador de Tráfico Vehicular en una Red de Carreteras

import networkx as nx
import matplotlib.pyplot as plt
import random

# -------------------------------
# 1. MODELADO DE LA RED DE TRÁFICO
# -------------------------------
def crear_red_ejemplo():
    G = nx.DiGraph()
    # Agregar nodos y aristas con capacidad
    edges = [
        ('Gran Via', 'Alcala', 10),
        ('Gran Via', 'Serrano', 5),
        ('Alcala', 'Serrano', 15),
        ('Alcala', 'Castellana', 10),
        ('Serrano', 'Castellana', 10),
        ('Serrano', 'Goya', 5),
        ('Castellana', 'Principe de Vergara', 10),
        ('Goya', 'Principe de Vergara', 10),
        ('Principe de Vergara', 'Velazquez', 8),
        ('Velazquez', 'Recoletos', 6),
        ('Recoletos', 'Gran Via', 7)
    ]
    for u, v, cap in edges:
        G.add_edge(u, v, original_capacity=cap, capacity=cap, flow=0)
    return G

# -------------------------------
# 2. SIMULACIÓN DE FLUJO VEHICULAR
# -------------------------------
def ford_fulkerson(G, source, sink):
    try:
        flow_value, flow_dict = nx.maximum_flow(G, source, sink)
        for u in flow_dict:
            for v in flow_dict[u]:
                G[u][v]['flow'] = flow_dict[u][v]
        return flow_value
    except nx.NetworkXUnfeasible:
        print("No hay camino posible entre las calles seleccionadas.")
        return 0

# -------------------------------
# 3. VISUALIZACIÓN GRÁFICA
# -------------------------------
def visualizar_red(G):
    pos = nx.spring_layout(G, seed=42)
    edge_labels = {(u, v): f"{G[u][v]['flow']}/{G[u][v]['capacity']}" for u, v in G.edges()}
    colores = ["red" if G[u][v]['flow'] >= G[u][v]['capacity'] and G[u][v]['capacity'] > 0 else "green" for u, v in G.edges()]

    nx.draw(G, pos, with_labels=True, edge_color=colores, node_color='lightblue', node_size=1500, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
    plt.title("Red de Tráfico - Flujo / Capacidad")
    plt.show()

# -------------------------------
# 4. EVENTOS ALEATORIOS
# -------------------------------
def simular_accidente(G):
    aristas = list(G.edges())
    if not aristas:
        print("No hay carreteras en la red.")
        return
    u, v = random.choice(aristas)
    G[u][v]['capacity'] = 0
    G[u][v]['flow'] = 0
    print(f"Accidente simulado: carretera entre {u} y {v} cerrada.")

# -------------------------------
# 5. INTERFAZ
# -------------------------------
def menu():
    G = crear_red_ejemplo()
    while True:
        print("\nSimulador de Tráfico Vehicular")
        print("1. Mostrar red de carreteras")
        print("2. Calcular flujo máximo")
        print("3. Cerrar una carretera")
        print("4. Reabrir una carretera")
        print("5. Simular accidente aleatorio")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            visualizar_red(G)

        elif opcion == '2':
            origen = input("Calle origen: ")
            destino = input("Calle destino: ")
            if origen in G.nodes and destino in G.nodes:
                flujo = ford_fulkerson(G, origen, destino)
                print(f"Flujo máximo desde {origen} a {destino}: {flujo}")
                visualizar_red(G)
            else:
                print("Calles inválidas.")

        elif opcion == '3':
            u = input("Calle origen de la carretera a cerrar: ")
            v = input("Calle destino: ")
            if G.has_edge(u, v):
                G[u][v]['capacity'] = 0
                G[u][v]['flow'] = 0
                print(f"Carretera de {u} a {v} cerrada.")
            else:
                print("Esa carretera no existe.")

        elif opcion == '4':
            u = input("Calle origen de la carretera a reabrir: ")
            v = input("Calle destino: ")
            if G.has_edge(u, v):
                G[u][v]['capacity'] = G[u][v]['original_capacity']
                print(f"Carretera de {u} a {v} reabierta con capacidad {G[u][v]['capacity']}.")
            else:
                print("Esa carretera no existe.")

        elif opcion == '5':
            simular_accidente(G)

        elif opcion == '6':
            break

        else:
            print("Opción inválida.")

if __name__ == '__main__':
    menu()
