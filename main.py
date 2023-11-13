import networkx as nx
import random
from collections import Counter
import numpy as np
from matplotlib import pyplot as plt

def read_graph(filename):
    G = nx.MultiGraph() # Tworzenie grafu
    with open(filename, 'r') as file:
        for line in file:
            edge = tuple(map(int, line.split()))  # Rozdzielanie liczby na krawędziach
            G.add_edge(*edge)  # Dodawanie krawędzi do grafu
    return G
def graph_info(G,a):
    print ("Zadanie "+a)
    print("Liczba węzłów w przekazanym grafie:", G.number_of_nodes())
    print("Liczba krawędzi w przekazanym grafie:", G.number_of_edges())
def largest_connected_graph(G):
     # Stwórz nowy graf zawierający tylko największą składową spójną


    return largest_connected_component
if __name__ == '__main__':
# 1a)
    original_graph = read_graph('2.txt') #wczytanie grafu z pliku
    graph_info(original_graph,'1a') #wypisanie liczby wezlow i liczby krawedzi
# 1b)
    reduced_graph = nx.Graph(original_graph) #usunięcie liczby wezlow
    reduced_graph.remove_edges_from(nx.selfloop_edges(original_graph)) #usunięcie pętli
    graph_info(reduced_graph,'1b')  # wypisanie liczby wezlow i liczby krawedzi

# 2)
    largest_connected_component = reduced_graph.subgraph(max(nx.connected_components(reduced_graph), key=len))
    graph_info(largest_connected_component,'2')  # wypisanie liczby wezlow i liczby krawedzi
# 3)
    probs = [100,1000,10000]
    paths = []
    for prob in probs:
        for i in range(prob):
            random_nodes = random.sample(list(largest_connected_component.nodes()), 2)
            start_node, end_node = random_nodes
            path = nx.shortest_path_length(largest_connected_component, start_node, end_node)
            #print(path)
            paths.append(path)
        average_path_length = sum(paths) / prob
        print(f"próba {prob} średnia długość ścieżki {average_path_length:.2f}")
