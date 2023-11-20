import networkx as nx
import random
from collections import Counter
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

def read_graph(filename):
    G = nx.MultiGraph() # Tworzenie grafu
    with open(filename, 'r') as file:
        for line in file:
            edge = tuple(map(int, line.split()))  # Rozdzielanie liczby na krawędziach
            G.add_edge(*edge)  # Dodawanie krawędzi do grafu
    return G
def graph_info(G):
    print("Liczba węzłów w przekazanym grafie:", G.number_of_nodes())
    print("Liczba krawędzi w przekazanym grafie:", G.number_of_edges())
def largest_connected_graph(G):
     # Stwórz nowy graf zawierający tylko największą składową spójną
    return largest_connected_component

if __name__ == '__main__':
# 1a)
    print("Zadanie 1a")
    original_graph = read_graph('2.txt') #wczytanie grafu z pliku
    graph_info(original_graph) #wypisanie liczby wezlow i liczby krawedzi
# 1b)
    print("\nZadanie 1b")
    reduced_graph = nx.Graph(original_graph) #usunięcie liczby wezlow
    reduced_graph.remove_edges_from(nx.selfloop_edges(original_graph)) #usunięcie pętli
    graph_info(reduced_graph)  # wypisanie liczby wezlow i liczby krawedzi

# 2)
    print("\nZadanie 2")
    largest_connected_component = reduced_graph.subgraph(max(nx.connected_components(reduced_graph), key=len))
    graph_info(largest_connected_component)  # wypisanie liczby wezlow i liczby krawedzi
# 3)
    print("\nZadanie 3 ")
    probs = [100,1000,10000]
    paths = []
    for prob in probs:
        for i in range(prob):
            random_nodes = random.sample(list(largest_connected_component.nodes()), 2)
            start_node, end_node = random_nodes
            path = nx.shortest_path_length(largest_connected_component, start_node, end_node)
            paths.append(path)
        average_path_length = sum(paths) / prob
        print(f"próba {prob} średnia długość ścieżki {average_path_length:.2f}")
# 4)
    print("\nZadanie 4 ")
    core_numbers = nx.core_number(reduced_graph) #zwroci słownik -> liczbe wszystkich rdzeni w grafie, możliwa do usyzkania
    max_core_number = max(core_numbers.values())
    core_numbers_list = list(sorted(Counter(core_numbers.values()).items(), reverse=True))
    print(f"Rdzeni o największym możliwym rzędzie - {core_numbers_list[0][0]} jest {core_numbers_list[0][1]}")
    print(f"Rdzeni o drugiej największym możliwym rzędzie - {core_numbers_list[1][0]} jest {core_numbers_list[0][1]+core_numbers_list[1][1]}")
    print(f"Rdzeni o trzecim największym możliwym rzędzie - {core_numbers_list[2][0]} jest {core_numbers_list[0][1]+core_numbers_list[1][1]+core_numbers_list[2][1]}")
# 5)
    print("\nZadanie 5 ")
    degrees = dict(reduced_graph.degree()) #degrees = (node,degree)
    values_degrees = list(degrees.values()) #zebrane stopnie wezlow
    values_degrees_counted = (Counter(values_degrees)) #(stopien, liczba wystapien wezlow o danymstopniu)
    deg, num = zip(*values_degrees_counted.items())

    plt.plot(deg, num, '.')
    plt.title("Rozkład stopni wierzchołków")
    plt.xlabel("Stopień wierzchołka")
    plt.ylabel("Liczba wierzchołków o danym stopniu")
    plt.savefig('wyk1.png')
    plt.show()

    plt.loglog(deg, num, '.')
    plt.title("Rozkład stopni wierzchołków w skali podwójnie logarytmicznej")
    plt.xlabel("Stopień wierzchołka")
    plt.ylabel("Liczba wierzchołków o danym stopniu")
    plt.savefig('wyk2.png')
    plt.show()

# 6)
    print("\nZadanie 6 ")
    bins = np.logspace(np.log10(min(values_degrees)), np.log10(max(values_degrees)), 20)
    node6, degree6 = np.histogram(values_degrees, bins=bins)    #rozlokowanie logarytmiczne przedzialow

    plt.loglog(degree6[:-1], node6, 'o') #node6 oraz degree6 mają różną liczność
    plt.xlabel("Stopień wierzchołka")
    plt.ylabel("Liczba wierzchołków o danym stopniu")
    plt.title("Rozkład stopni wierzchołków w skali podwójnie logarytmicznej\n"
              " z przedziałami rozlokowanymi logarytmicznie")
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='gray')
    plt.savefig('wyk3.png')
    plt.show()

    node6 = np.append(node6, 0)  # poniewaz nie zgadza sie liczba node6 i degree6
    cumulative_distribution = np.cumsum(node6) / np.sum(node6) #dystrybuanta
    complementary_cumulative_distribution = 1 - cumulative_distribution #dopelnienie dystrybuanty

    plt.loglog(degree6, complementary_cumulative_distribution, 'o')
    plt.title(
        "Dopełnienie dystrybuant rozkładu stopni wierzchołków")
    plt.xlabel("Stopień wierzchołka")
    plt.ylabel("Liczba wierzchołków o danym stopniu")
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='gray')
    plt.savefig('wyk4.png')
    plt.show()

    zeros = np.where(complementary_cumulative_distribution == 0)[0]  #konieczność usunięcia wartosci 0 do wykorzystania funkcji polyfit i zadbania aby x i y byly rownoliczne
    xx = np.delete(degree6,zeros)
    yy = np.delete(complementary_cumulative_distribution, zeros)

    coefs = np.polyfit(np.log10(xx), np.log10(yy), 1)   #wspolczynniki regresjii dla wykresu podwojnie logarytmicznego
    y = 10 ** (np.log10(xx) * coefs[0] + coefs[1]) # podnosze do potegi ze wzgledu na to, ze potem przy rysowaniu brany jest logarytm

    plt.loglog(degree6, complementary_cumulative_distribution, 'o')
    plt.loglog(xx, y, color='red')
    plt.title(
        "Dopełnienie dystrybuant wraz z naniesioną krzywą regresjii")
    plt.xlabel("Stopień wierzchołka")
    plt.ylabel("Liczba wierzchołków o danym stopniu")
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='gray')
    plt.savefig('wyk5.png')
    plt.show()

    print("Wykładnik rozkładu potęgowego:", -coefs[0])

# 7)
    print("\nZadanie 7 ")

    d = sorted(values_degrees) #wszystkie stopnie dla kazdego wierzcholka
    N = len(d)
    gamma = np.ones(len(d)-1)
    for k in range(1,len(d)): #bo k nie moze byc 0 bo jest w mianowniku
        gamma[k-1] = (1/k)*np.sum(np.log(d[(N-k-1):])-np.log(d[N-k-1]))
    alfa = 1 + 1/gamma

    plt.plot(alfa)
    plt.ylabel("alfa(k)")
    plt.xlabel("k")
    plt.title("Wykres Hilla")
    plt.savefig('wyk6-hilla.png')
    plt.show()

    print("ALFA ", alfa[50:])
    plt.plot(alfa[40:])
    plt.ylabel("alfa(k)")
    plt.xlabel("k")
    plt.title("Wykres Hilla")
    plt.savefig('wyk7-hilla.png')
    plt.show()