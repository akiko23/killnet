# import csv
# from typing import TypeVar, Iterable, Optional


# Station = TypeVar('Station')


# class Road:
#     def init(
#             self,
#             quantity_limit: int,
#             tonnage_limit: float | int,
#             max_train_tonnage: float | int,
#     ):
#         self.tonnage_limit = tonnage_limit
#         self.quantity_limit = quantity_limit
#         self.max_train_tonnage = max_train_tonnage


# class Station:
#     def __init__(
#             self,
#             station_id: int,
#             to_roads: dict[Station, list[Road]],
#             from_roads: dict[Station, list[Road]]
#     ):
#         self.station_id = station_id
#         self.to_neighbours = to_neighbours
#         self.from_neighbours = from_neighbours

#     def __hash__(self):
#         return hash(self.station_id)


#     def __repr__(self):
#         return f"\nStation id: {self.station_id}\nFrom neighbours: {self.from_neighbours}\nTo neighbours: {self.to_neighbours}\n"


# roads: dict[int, set] = []
# with open('uploaded_file.csv') as dataset_file:
#     reader = csv.DictReader(dataset_file, delimiter=',')
#     for row in reader:
#         road_id_from, road_id_to = row['start'], row['end']
#         tonnage_limit, max_train_tonnage = row['tonnage_limit'], row['max_train_tonnage']
        
#         roads.append(
#             {
#                 'road_id_from': road_id_from,
#                 'road_id_to': road_id_to,
#                 'tonnage_limit': tonnage_limit,
#                 'max_train_tonnage': max_train_tonnage
#             }
#         )

#     print(roads)


# stations = set()
# for road in roads:
#     to_roads = list(filter(lambda r: r['road_id_from'] == road['road_id_from'], roads))
#     from_roads = list(filter(lambda r: r['road_id_to'] == road['road_id_from'], roads))
    

#     stations.add(
#         Station(
#             station_id=road['road_id_from'],
#             from_roads=from_roads,
#             to_roads=to_roads
#         )
#     )


import networkx as nx
import csv
import matplotlib.pyplot as plt


def change_quantity(quantity_limit, max_train_tonnage, tonnage_limit):
    while quantity_limit * max_train_tonnage > tonnage_limit:
        quantity_limit -= 1
    return quantity_limit



def draw_graph(csv_file_path: str):
    G = nx.DiGraph()
    stations = {}
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        for road in reader:
            road = road[2:]
            road.pop(2)
            road = [int(e) for e in road[:3]] + [float(e) for e in road[3:]]
            start, end, quantity_limit, tonnage_limit, max_train_tonnage = road
            quantity_limit = change_quantity(quantity_limit, max_train_tonnage, tonnage_limit)

            if start not in stations:
                stations[start] = {}
            if end not in stations[start]:
                stations[start][end] = [0, 0]
            stations[start][end][0] = quantity_limit

            if end not in stations:
                stations[end] = {}
            if start not in stations[end]:
                stations[end][start] = [0, 0]
            stations[end][start][1] = quantity_limit


    checked_roads = []
    stations = {e: stations[e] for e in sorted(stations, key=lambda x: len(stations[x]))}
    G.add_nodes_from(set(stations.keys()))
    for id1, roads in stations.items():
        trains = sum([neighbour[1]-neighbour[0] for neighbour in roads.values()])
        pos = int(trains > 0)
        if trains < 0:
            trains *= -1
        p = [1, 0]
        for id__, road in roads.items():
            if id1 not in checked_roads:
                if trains <= road[pos]:
                    stations[id1][id__][pos] -= trains
                    stations[id__][id1][p[pos]] -= trains
                    break
                else:
                    trains -= road[pos]
                    stations[id1][id__][pos] = 0
                    stations[id__][id1][p[pos]] = 0

        stations[id1] = roads


    for state in stations:
        [G.add_edge(state, st, description=stations[state][st][0]) for st in stations[state] if stations[state][st][0] != 0]

    # Отрисовываем граф
    pos = nx.spring_layout(G, seed=0)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", arrows=True, connectionstyle="arc3, rad = 0.1")

    # Визуализируем имена рёбер на графе
    edge_labels = {(u, v): d["description"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.3, font_color='black')
    plt.title("Граф с именами рёбер")
    plt.show()


def save_image(data_path: str, output_image_name: str) -> None:
    stations = []
    G = nx.DiGraph()

    with open(data_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for i in reader:
            if i[0]:
                stations += i[2:4]
                G.add_edge(i[2], i[3], description=i[5])
                print(i)
                print(i[2:4])


    G.add_nodes_from(set(stations))
    pos = nx.spring_layout(G, seed=0)
    nx.draw(G, pos, with_labels=True,
            arrowsize=6,
            font_size=1,
            node_size=50,
            node_color="skyblue",
            arrows=True,
            connectionstyle="arc3, rad = 0.1")

    # Визуализируем имена рёбер на графе
    edge_labels = {(u, v): d["description"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=2, label_pos=0.4, font_color='black')
    plt.savefig(output_image_name, format="PNG", dpi=1000, bbox_inches='tight')



def change_quantity(quantity_limit, max_train_tonnage, tonnage_limit):
    while quantity_limit * max_train_tonnage > tonnage_limit:
        quantity_limit -= 1
    return quantity_limit


def save_correct_csv(input_dataset, output_dataset, output_image):
    G = nx.DiGraph()
    stations = {}
    with open(input_dataset, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        for road in reader:
            road = road[2:]
            road.pop(2)
            road = [int(e) for e in road[:3]] + [float(e) for e in road[3:]]
            start, end, quantity_limit, tonnage_limit, max_train_tonnage = road
            quantity_limit = change_quantity(quantity_limit, max_train_tonnage, tonnage_limit)

            if start not in stations:
                stations[start] = {}
            if end not in stations[start]:
                stations[start][end] = [0, 0]
            stations[start][end][0] = quantity_limit

            if end not in stations:
                stations[end] = {}
            if start not in stations[end]:
                stations[end][start] = [0, 0]
            stations[end][start][1] = quantity_limit

    checked_roads = []
    stations = {e: stations[e] for e in sorted(stations, key=lambda x: len(stations[x]))}
    G.add_nodes_from(set(stations.keys()))
    for id1, roads in stations.items():
        trains = sum([neighbour[1] - neighbour[0] for neighbour in roads.values()])
        pos = int(trains > 0)
        if trains < 0:
            trains *= -1
        p = [1, 0]
        for id__, road in roads.items():
            if id1 not in checked_roads:
                if trains <= road[pos]:
                    stations[id1][id__][pos] -= trains
                    stations[id__][id1][p[pos]] -= trains
                    break
                else:
                    trains -= road[pos]
                    stations[id1][id__][pos] = 0
                    stations[id__][id1][p[pos]] = 0

        stations[id1] = roads

    for state in stations:
        [G.add_edge(state, st, description=stations[state][st][0]) for st in stations[state] if stations[state][st][0] != 0]

    # Отрисовываем граф
    pos = nx.spring_layout(G, seed=0)
    nx.draw(G, pos, with_labels=True,
            arrowsize=6,
            font_size=1,
            node_size=50,
            node_color="skyblue",
            arrows=True,
            connectionstyle="arc3, rad = 0.1")

    # Визуализируем имена рёбер на графе
    edge_labels = {(u, v): d["description"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=2, label_pos=0.4, font_color='black')
    plt.savefig(output_image, format="PNG", dpi=1000, bbox_inches='tight')

    with open(input_dataset, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        with open(output_dataset, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for data in reader:
                data[5] = str(stations[int(data[2])][int(data[3])][0])
                writer.writerow(data)
