# TSP Experiment (Python)

A console starter for the Science of Computing & Digital Media extension. Dataset loading, route validation, timing and brute force are supplied. Your tasks are to implement nearest neighbour and attempt 2-opt, then investigate their results.

## Getting started

Requires Python 3.10 or later. No extra packages are needed.

Add the supplied Data folder beside main.py, then run:

```bash
python main.py
```

On systems where Python is named python3, use python3 main.py.

## Project structure

| File | Purpose |
|---|---|
| main.py | Experiment settings, timing and console output |
| tsp.py | Dataset reader, distance matrix, route cost and validation |
| brute_force.py | Supplied exact solver for up to 10 cities |
| student_algorithms.py | Your nearest-neighbour and 2-opt implementations |

## Select a dataset

Edit the settings at the top of main.py:

```python
dataset_file = "Data/eil51.tsp"
start_city = 0
known_optimal_cost = 426
```

Use the reference cost for the exact selected file, or None if unknown. Small instances obtain their optimum automatically from brute force. See DATA_README.md for the supplied files.

Paths are relative to main.py. No build or file-copy step is required. The loader supports symmetric TSPLIB TSP files using EUC_2D distances. It rounds each distance to the nearest integer with .5 upwards, matching the C# starter.

## Where to extend

Replace the two NotImplementedError statements in student_algorithms.py with your implementations:

```python
def nearest_neighbour(distances: list[list[float]], start_city: int) -> list[int]:
def two_opt(distances: list[list[float]], initial_route: list[int]) -> list[int]:
```

Use distances[from_city][to_city] to look up a distance. Return a list of city indices, each appearing once, with the requested starting city first. Do not append the start again: route_cost adds the return journey. Indices start at 0; displayed file IDs start at 1.

For 2-opt, copy the supplied route before editing it. Preserve its starting city and return a route no worse than the original.

In main.py, set run_nearest_neighbour to True when ready, followed by run_two_opt when ready. The calls, timing and output are already connected. There is no need to change the supplied loader or brute-force solver.

The runner uses one starting city. To investigate starting-city effects, add a loop to run nearest neighbour from every city for at least one dataset. Document your tie rule.

A serious, tested attempt at 2-opt is valuable even if incomplete. Explain what works, what fails and what your evidence supports.

## Measurements

Each enabled algorithm gets an untimed warm-up and one timed run. Validation and final reporting are outside the timed section. Repeat runs and record results yourself; CSV export is not supplied.

Brute force generates (n-1)! permutations and evaluates (n-1)! / 2 unique symmetric tours for n >= 3. For two cities it evaluates one tour. Above 10 cities it is skipped, so enable a student algorithm to obtain a route.

For 2-opt, the output distinguishes refinement time from the combined nearest-neighbour and refinement time. Route validation checks tour structure; it does not establish that a heuristic or its stopping condition is correct.

The Python and C# versions use the same search and counting rules, but their execution times will differ. Use one language consistently within a timing comparison.
