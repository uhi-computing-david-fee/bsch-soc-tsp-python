"""Supplied exact baseline, mirroring the C# recursive search."""
from math import isfinite
from tsp import route_cost


def solve(distances: list[list[float]], start_city: int) -> tuple[list[int], int]:
    city_count = len(distances)
    if city_count < 2 or any(len(row) != city_count for row in distances):
        raise ValueError("Distances must be a square matrix with at least two cities.")
    if not 0 <= start_city < city_count:
        raise ValueError("Starting city is out of range.")
    if city_count > 10:
        raise ValueError("Brute force is limited to 10 cities.")
    for i in range(city_count):
        for j in range(city_count):
            if not isfinite(distances[i][j]) or distances[i][j] < 0:
                raise ValueError("Distances must be finite and non-negative.")
            if distances[i][j] != distances[j][i]:
                raise ValueError("Removing reverse duplicates requires symmetric distances.")

    route = [start_city] + [city for city in range(city_count) if city != start_city]
    best_route = []
    best_cost = float("inf")
    tours_evaluated = 0

    def search(next_position: int) -> None:
        # These variables belong to solve(), and are updated by this local function.
        nonlocal best_route, best_cost, tours_evaluated
        if next_position == city_count:
            # Keep only one orientation of each symmetric tour.
            if city_count > 2 and route[1] > route[-1]:
                return
            cost = route_cost(distances, route)
            tours_evaluated += 1
            if not isfinite(cost):
                raise ValueError("The total route cost is too large.")
            if cost < best_cost:
                best_cost = cost
                best_route = route.copy()
            return

        for i in range(next_position, city_count):
            # Choose, explore, then undo the swap.
            route[next_position], route[i] = route[i], route[next_position]
            search(next_position + 1)
            route[next_position], route[i] = route[i], route[next_position]

    search(1)
    # For n >= 3: (n-1)! permutations generated, (n-1)! / 2 tours evaluated.
    # Python returns both values as a tuple, replacing C#'s out parameter.
    return best_route, tours_evaluated
