"""Supplied TSPLIB reader, distance calculation and route checks."""
from math import floor, isfinite, sqrt
from pathlib import Path


def load_distances(path: str | Path) -> list[list[float]]:
    # File IDs 1..n map to indices 0..n-1, regardless of row order.
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    headers = {}
    coordinate_start = None
    for index, raw in enumerate(lines):
        line = raw.strip()
        if not line:
            continue
        if line.upper() == "NODE_COORD_SECTION":
            coordinate_start = index + 1
            break
        if line.upper().endswith("_SECTION"):
            raise ValueError("Expected NODE_COORD_SECTION; only EUC_2D files are supported.")
        parts = line.split(":", 1) if ":" in line else line.split(maxsplit=1)
        if len(parts) == 2:
            headers[parts[0].strip().upper()] = parts[1].strip()

    if headers.get("TYPE", "").upper() != "TSP":
        raise ValueError("Use a symmetric TSPLIB file with TYPE: TSP.")
    if headers.get("EDGE_WEIGHT_TYPE", "").upper() != "EUC_2D":
        raise ValueError("Use EDGE_WEIGHT_TYPE: EUC_2D.")
    try:
        city_count = int(headers.get("DIMENSION", ""))
    except ValueError:
        raise ValueError("DIMENSION must specify at least two cities.") from None
    if city_count < 2:
        raise ValueError("DIMENSION must specify at least two cities.")
    if "EDGE_DATA_FORMAT" in headers:
        raise ValueError("Restricted-edge instances are not supported.")
    if coordinate_start is None:
        raise ValueError("Missing NODE_COORD_SECTION.")

    coordinates = [None] * city_count
    for index in range(coordinate_start, len(lines)):
        line = lines[index].strip()
        if not line:
            continue
        if line.upper() == "EOF":
            break
        if line.upper() == "DISPLAY_DATA_SECTION":
            for extra in lines[index:]:
                section = extra.strip().upper()
                if section.endswith("_SECTION") and section != "DISPLAY_DATA_SECTION":
                    raise ValueError("Extra problem sections are not supported.")
            break
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(f"Invalid coordinate row: {line}")
        try:
            city_id = int(parts[0])
            x, y = float(parts[1]), float(parts[2])
        except ValueError:
            raise ValueError(f"Invalid coordinate row: {line}") from None
        if not 1 <= city_id <= city_count:
            raise ValueError(f"Invalid city ID: {city_id}")
        if coordinates[city_id - 1] is not None:
            raise ValueError(f"City {city_id} is repeated.")
        if not isfinite(x) or not isfinite(y):
            raise ValueError(f"Invalid coordinates for city {city_id}.")
        coordinates[city_id - 1] = (x, y)
    if any(point is None for point in coordinates):
        raise ValueError("Coordinate count does not match DIMENSION.")

    distances = [[0.0] * city_count for _ in range(city_count)]
    for i in range(city_count):
        for j in range(i + 1, city_count):
            dx = coordinates[i][0] - coordinates[j][0]
            dy = coordinates[i][1] - coordinates[j][1]
            distance = sqrt(dx * dx + dy * dy)
            if not isfinite(distance):
                raise ValueError("Coordinates are too large.")
            # TSPLIB rounds .5 upwards. Python's round() uses a different rule.
            distances[i][j] = distances[j][i] = float(floor(distance + 0.5))
    return distances


def route_cost(distances: list[list[float]], route: list[int]) -> float:
    # Store each city once; add the return journey here.
    cost = 0.0
    for i in range(len(route) - 1):
        cost += distances[route[i]][route[i + 1]]
    cost += distances[route[-1]][route[0]]
    return cost


def validate_route(distances: list[list[float]], route: list[int], start_city: int) -> None:
    city_count = len(distances)
    if city_count < 2 or any(len(row) != city_count for row in distances):
        raise ValueError("Distances must be a square matrix with at least two cities.")
    if not 0 <= start_city < city_count:
        raise ValueError("Starting city is out of range.")
    if not isinstance(route, list) or len(route) != city_count:
        raise ValueError("Return a list containing every city exactly once.")
    if route[0] != start_city:
        raise ValueError("The route must begin at the requested starting city.")
    visited = [False] * city_count
    for city in route:
        if type(city) is not int or not 0 <= city < city_count or visited[city]:
            raise ValueError("The route contains an invalid or repeated city.")
        visited[city] = True
