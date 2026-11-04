"""Run this file. Edit the experiment settings below."""
from math import isfinite
from pathlib import Path
from time import perf_counter
import brute_force
import student_algorithms
from tsp import load_distances, route_cost, validate_route

# EXPERIMENT SETTINGS
dataset_file = "Data/example-four.tsp"
start_city = 0                    # Index 0 corresponds to file city 1.
known_optimal_cost = None          # Reference for this EXACT dataset, e.g. 426.
run_nearest_neighbour = False      # Enable after implementing task 1.
run_two_opt = False                # Also requires nearest neighbour.


def print_result(name, route, cost, milliseconds):
    print(name)
    print("Route (file IDs): " + " -> ".join(str(city + 1) for city in route + [route[0]]))
    print(f"Total cost: {cost:.3f}")
    print(f"Elapsed time: {milliseconds:.6f} ms")


def print_gap(cost, optimum):
    if optimum is not None and cost < optimum:
        raise ValueError("Route cost is below the supplied optimum. Check your reference.")
    if optimum is not None and optimum > 0:
        print(f"Optimality gap: {100 * (cost - optimum) / optimum:.2f}%\n")
    else:
        print("Optimality gap unavailable (unknown or zero optimum).\n")


def main():
    # Resolve Data relative to this script, even when launched from elsewhere.
    distances = load_distances(Path(__file__).resolve().parent / dataset_file)
    city_count = len(distances)
    if not 0 <= start_city < city_count:
        raise ValueError("Starting city is out of range.")
    if run_two_opt and not run_nearest_neighbour:
        raise ValueError("Enable nearest neighbour before 2-opt.")
    if known_optimal_cost is not None and (not isfinite(known_optimal_cost) or known_optimal_cost < 0):
        raise ValueError("A known optimum must be finite and non-negative.")

    print(f"Dataset: {dataset_file} | Cities: {city_count} | Start city (file ID): {start_city + 1}")
    print("TSPLIB EUC_2D: symmetric distances rounded to integers\n")
    optimal_cost = known_optimal_cost

    if city_count <= 10:
        brute_force.solve(distances, start_city)  # Untimed warm-up, as in C#.
        started = perf_counter()
        exact_route, tours_evaluated = brute_force.solve(distances, start_city)
        milliseconds = (perf_counter() - started) * 1000
        validate_route(distances, exact_route, start_city)
        exact_cost = route_cost(distances, exact_route)
        if known_optimal_cost is not None and known_optimal_cost != exact_cost:
            raise ValueError("The supplied optimum does not match exhaustive search.")
        optimal_cost = exact_cost
        print_result("Brute force", exact_route, exact_cost, milliseconds)
        print(f"Unique tours evaluated: {tours_evaluated}\n")
    else:
        print("Brute force skipped above 10 cities.\n")
        if optimal_cost is None:
            print("No published optimum supplied; optimality gaps will be unavailable.\n")

    if not run_nearest_neighbour:
        print("Nearest neighbour and 2-opt are disabled until implemented.\n")
    if run_nearest_neighbour:
        student_algorithms.nearest_neighbour(distances, start_city)
        started = perf_counter()
        nearest_route = student_algorithms.nearest_neighbour(distances, start_city)
        nearest_ms = (perf_counter() - started) * 1000
        validate_route(distances, nearest_route, start_city)
        nearest_cost = route_cost(distances, nearest_route)
        print_result("Nearest neighbour", nearest_route, nearest_cost, nearest_ms)
        print_gap(nearest_cost, optimal_cost)

        if run_two_opt:
            student_algorithms.two_opt(distances, nearest_route.copy())
            refinement_input = nearest_route.copy()
            started = perf_counter()
            improved_route = student_algorithms.two_opt(distances, refinement_input)
            refinement_ms = (perf_counter() - started) * 1000
            validate_route(distances, improved_route, start_city)
            improved_cost = route_cost(distances, improved_route)
            if improved_cost > nearest_cost + 1e-9 * max(1, nearest_cost):
                raise ValueError("2-opt returned a worse route.")
            print_result("2-opt (refinement only)", improved_route, improved_cost, refinement_ms)
            print_gap(improved_cost, optimal_cost)
            print(f"Cost reduction from nearest neighbour: {nearest_cost - improved_cost:.3f}")
            print(f"Construction + refinement time: {nearest_ms + refinement_ms:.6f} ms")


if __name__ == "__main__":
    main()
