import random
import math
from typing import Dict, Any, List

# Parámetros del problema (constantes)
DESTINATIONS = {
    1: (10, 10, 4),
    2: (20, 15, 6),
    3: (15, 25, 3),
    4: (30, 10, 2),
    5: (25, 30, 5),
    6: (40, 20, 3),
    7: (12, 18, 4),
    8: (18, 22, 5),
    9: (35, 25, 6),
    10: (22, 12, 2),
    11: (17, 8, 3),
    12: (28, 18, 4),
}
NUM_VEHICLES_DEFAULT = 4
VEHICLE_CAPACITY_DEFAULT = 15

# Parámetros por defecto del algoritmo genético
POP_SIZE_DEFAULT        = 100
GENERATIONS_DEFAULT     = 500
MUTATION_RATE_DEFAULT   = 0.15
TOURNAMENT_K_DEFAULT    = 2
ELITE_SIZE_DEFAULT      = 2
REINIT_INTERVAL_DEFAULT = 50
REINIT_RATE_DEFAULT     = 0.1


def init_population(pop_size: int, num_vehicles: int, destinations: Dict[int, Any]) -> List[List[List[int]]]:
    dest_ids = list(destinations.keys())
    population = []
    for _ in range(pop_size):
        random.shuffle(dest_ids)
        avg = len(dest_ids) / float(num_vehicles)
        individual = [dest_ids[int(i * avg): int((i + 1) * avg)] for i in range(num_vehicles)]
        population.append(individual)
    return population


def fitness(individual: List[List[int]], destinations: Dict[int, Any], vehicle_capacity: int) -> float:
    def euclidean(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def route_distance(route):
        if not route:
            return 0
        dist, prev = 0, (0, 0)
        for node in route:
            coord = destinations[node][:2]
            dist += euclidean(prev, coord)
            prev = coord
        return dist + euclidean(prev, (0, 0))

    def exceeds_capacity(route):
        total_demand = sum(destinations[n][2] for n in route)
        return total_demand > vehicle_capacity

    total_cost = 0
    for route in individual:
        if exceeds_capacity(route):
            return float('inf')
        total_cost += route_distance(route)
    return total_cost


def tournament_selection(population: List[List[List[int]]], fitnesses: List[float], k: int) -> List[List[int]]:
    if k > len(population):
        raise ValueError("El tamaño del torneo 'k' no puede ser mayor que la población.")
    candidatos = list(zip(population, fitnesses))
    contenders = random.sample(candidatos, k)
    ganador = min(contenders, key=lambda x: x[1])[0]
    return ganador


def crossover(parent1, parent2, destinations, vehicle_capacity):
    child = []
    for r1, r2 in zip(parent1, parent2):
        child.append(r1.copy() if random.random() < 0.5 else r2.copy())

    def repair(ind):
        flat = [d for route in ind for d in route]
        duplicates = set(d for d in flat if flat.count(d) > 1)
        for route in ind:
            new_route = [d for d in route if d not in duplicates]
            route[:] = new_route
            duplicates -= set(new_route)
        assigned = {d for route in ind for d in route}
        missing = list(set(destinations.keys()) - assigned)
        for d in missing:
            sorted_routes = sorted(ind, key=lambda r: sum(destinations[n][2] for n in r))
            for route in sorted_routes:
                if sum(destinations[n][2] for n in route) + destinations[d][2] <= vehicle_capacity:
                    route.append(d)
                    break
            else:
                sorted_routes[0].append(d)
        return ind

    return repair(child)


def mutate(individual, mutation_rate):
    for _ in range(len(individual)):
        if random.random() < mutation_rate:
            r1, r2 = random.sample(range(len(individual)), 2)
            if individual[r1] and individual[r2]:
                i1 = random.randrange(len(individual[r1]))
                i2 = random.randrange(len(individual[r2]))
                individual[r1][i1], individual[r2][i2] = individual[r2][i2], individual[r1][i1]
    return individual


def route_distance(route, destinations):
    def euclidean(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])
    if not route:
        return 0.0
    dist, prev = 0.0, (0, 0)
    for node in route:
        coord = destinations[node][:2]
        dist += euclidean(prev, coord)
        prev = coord
    return dist + euclidean(prev, (0, 0))


def _run_full_genetic(params: Dict[str, Any]) -> Dict[str, Any]:
    pop_size        = params.get("population_size", POP_SIZE_DEFAULT)
    generations     = params.get("generations", GENERATIONS_DEFAULT)
    mutation_rate   = params.get("mutation_rate", MUTATION_RATE_DEFAULT)
    tournament_k    = params.get("tournament_k", TOURNAMENT_K_DEFAULT)
    elite_size      = params.get("elite_size", ELITE_SIZE_DEFAULT)
    reinit_interval = params.get("reinit_interval", REINIT_INTERVAL_DEFAULT)
    reinit_rate     = params.get("reinit_rate", REINIT_RATE_DEFAULT)
    num_vehicles    = params.get("num_vehicles", NUM_VEHICLES_DEFAULT)
    vehicle_capacity= params.get("vehicle_capacity", VEHICLE_CAPACITY_DEFAULT)

    population = init_population(pop_size, num_vehicles, DESTINATIONS)
    history = []
    best_solution = None
    best_fit = float('inf')
    first_epoch_info = None

    for gen in range(1, generations + 1):
        fits = [fitness(ind, DESTINATIONS, vehicle_capacity) for ind in population]

        # Guardar la primera generación
        if gen == 1:
            best1 = min(fits)
            avg1  = sum(fits) / len(fits)
            first_epoch_info = {
                "best": best1 if math.isfinite(best1) else None,
                "avg":  avg1  if math.isfinite(avg1) else None,
                "population": population.copy()
            }

        elites = [ind for _, ind in sorted(zip(fits, population))][:elite_size]
        for f, ind in zip(fits, population):
            if f < best_fit:
                best_fit = f
                best_solution = ind

        min_fit = min(fits)
        avg_fit = sum(fits) / len(fits)
        history.append({
            "gen": gen,
            "best": min_fit if math.isfinite(min_fit) else None,
            "avg":  avg_fit if math.isfinite(avg_fit) else None
        })

        new_pop = elites.copy()
        while len(new_pop) < pop_size:
            p1 = tournament_selection(population, fits, tournament_k)
            p2 = tournament_selection(population, fits, tournament_k)
            child = crossover(p1, p2, DESTINATIONS, vehicle_capacity)
            child = mutate(child, mutation_rate)
            new_pop.append(child)

        if gen % reinit_interval == 0:
            n_reinit = int(pop_size * reinit_rate)
            new_pop[-n_reinit:] = init_population(n_reinit, num_vehicles, DESTINATIONS)

        population = new_pop

    total_distance = sum(
        route_distance(route, DESTINATIONS)
        for route in best_solution
    )

    return {
        "history": history,
        "first_epoch": first_epoch_info,
        "final": {
            "best_solution": best_solution,
            "total_distance": total_distance
        }
    }


def run_genetic(params: Dict[str, Any], verbosity: str) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo genético con los parámetros dados.

    :param params: Diccionario con:
      - population_size, generations, mutation_rate, tournament_k, etc.
    :param verbosity: "first"|"all"|"final"
    :return: Resultados con historial, primera generación y solución final.
    """
    raw = _run_full_genetic(params)
    result: Dict[str, Any] = {}
    if verbosity in ("all",):
        result["history"] = raw["history"]
    if verbosity in ("first", "all"):
        result["first_epoch"] = raw["first_epoch"]
    result["final"] = raw["final"]
    return result
