"""Add your two implementations here. The runner is already connected to them."""


def nearest_neighbour(distances: list[list[float]], start_city: int) -> list[int]:
    # TASK 1: construct a tour from the requested starting city.
    # Use distances[from_city][to_city] and choose a consistent tie rule.
    # Return every city once; do not append the start again.
    raise NotImplementedError("Implement nearest neighbour here.")


def two_opt(distances: list[list[float]], initial_route: list[int]) -> list[int]:
    # TASK 2: improve the supplied nearest-neighbour tour.
    # Copy initial_route before editing: route = initial_route.copy()
    # Preserve its starting city, and do not worsen its cost.
    # Explain your move-selection and stopping policy.
    raise NotImplementedError("Implement 2-opt here.")
