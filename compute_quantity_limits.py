import csv
from typing import TypeVar, Iterable, Optional


Station = TypeVar('Station')


class Road:
    def init(
            self,
            quantity_limit: int,
            tonnage_limit: float | int,
            max_train_tonnage: float | int,
    ):
        self.tonnage_limit = tonnage_limit
        self.quantity_limit = quantity_limit
        self.max_train_tonnage = max_train_tonnage


class Station:
    def __init__(
            self,
            station_id: int,
            to_roads: dict[Station, list[Road]],
            from_roads: dict[Station, list[Road]]
    ):
        self.station_id = station_id
        self.to_neighbours = to_neighbours
        self.from_neighbours = from_neighbours

    def __hash__(self):
        return hash(self.station_id)


    def __repr__(self):
        return f"\nStation id: {self.station_id}\nFrom neighbours: {self.from_neighbours}\nTo neighbours: {self.to_neighbours}\n"


roads: dict[int, set] = []
with open('uploaded_file.csv') as dataset_file:
    reader = csv.DictReader(dataset_file, delimiter=',')
    for row in reader:
        road_id_from, road_id_to = row['start'], row['end']
        tonnage_limit, max_train_tonnage = row['tonnage_limit'], row['max_train_tonnage']
        
        roads.append(
            {
                'road_id_from': road_id_from,
                'road_id_to': road_id_to,
                'tonnage_limit': tonnage_limit,
                'max_train_tonnage': max_train_tonnage
            }
        )

    print(roads)


stations = set()
for road in roads:
    to_roads = list(filter(lambda r: r['road_id_from'] == road['road_id_from'], roads))
    from_roads = list(filter(lambda r: r['road_id_to'] == road['road_id_from'], roads))
    

    stations.add(
        Station(
            station_id=road['road_id_from'],
            from_roads=from_roads,
            to_roads=to_roads
        )
    )
    # print("Current:", road['road_id_from'])
    # print(neighbours_from)
    # print(neighbours_to)
    # print()


for station in stations:
    



