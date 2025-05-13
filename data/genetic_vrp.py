import random
import math

# Parámetros del problema
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
NUM_VEHICLES = 4
VEHICLE_CAPACITY = 15

# Parámetros del algoritmo genético
POP_SIZE         = 100
GENERATIONS      = 500
MUTATION_RATE    = 0.15
TOURNAMENT_K     = 2
ELITE_SIZE       = 2
REINIT_INTERVAL  = 50
REINIT_RATE      = 0.1

def init_population(pop_size, num_vehicles, destinations):
    dest_ids = list(destinations.keys())
    population = []
    for _ in range(pop_size):
        random.shuffle(dest_ids)
        avg = len(dest_ids) / float(num_vehicles)
        individual = [dest_ids[int(i * avg): int((i + 1) * avg)]
                      for i in range(num_vehicles)]
        population.append(individual)
    return population

def fitness(individual):
    def euclidean(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def route_distance(route):
        if not route:
            return 0
        dist, prev = 0, (0, 0)
        for node in route:
            coord = DESTINATIONS[node][:2]
            dist += euclidean(prev, coord)
            prev = coord
        return dist + euclidean(prev, (0, 0))

    def exceeds_capacity(route):
        total_demand = sum(DESTINATIONS[n][2] for n in route)
        return total_demand > VEHICLE_CAPACITY

    total_cost = 0
    for route in individual:
        if exceeds_capacity(route):
            return float('inf')
        total_cost += route_distance(route)
    return total_cost

def tournament_selection(population, fitnesses, k):
    if k > len(population):
        raise ValueError("k no puede ser mayor que la población.")
    candidates = list(zip(population, fitnesses))
    contenders  = random.sample(candidates, k)
    return min(contenders, key=lambda x: x[1])[0]

def crossover(parent1, parent2):
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
        missing  = list(set(DESTINATIONS.keys()) - assigned)
        for d in missing:
            sorted_routes = sorted(ind, key=lambda r: sum(DESTINATIONS[n][2] for n in r))
            for route in sorted_routes:
                if sum(DESTINATIONS[n][2] for n in route) + DESTINATIONS[d][2] <= VEHICLE_CAPACITY:
                    route.append(d)
                    break
            else:
                sorted_routes[0].append(d)
        return ind

    return repair(child)

def mutate(individual):
    for _ in range(len(individual)):
        if random.random() < MUTATION_RATE:
            r1, r2 = random.sample(range(len(individual)), 2)
            if individual[r1] and individual[r2]:
                i1 = random.randrange(len(individual[r1]))
                i2 = random.randrange(len(individual[r2]))
                individual[r1][i1], individual[r2][i2] = individual[r2][i2], individual[r1][i1]
    return individual

def genetic_vrp():
    population    = init_population(POP_SIZE, NUM_VEHICLES, DESTINATIONS)
    best_solution = None
    best_fit      = float('inf')

    for gen in range(1, GENERATIONS + 1):
        fits = [fitness(ind) for ind in population]
        # Elitismo
        elites = [ind for _, ind in sorted(zip(fits, population))][:ELITE_SIZE]
        for f, ind in zip(fits, population):
            if f < best_fit:
                best_fit      = f
                best_solution = ind

        new_pop = elites.copy()
        while len(new_pop) < POP_SIZE:
            p1    = tournament_selection(population, fits, TOURNAMENT_K)
            p2    = tournament_selection(population, fits, TOURNAMENT_K)
            child = crossover(p1, p2)
            new_pop.append(mutate(child))

        if gen % REINIT_INTERVAL == 0:
            n_reinit = int(POP_SIZE * REINIT_RATE)
            new_pop[-n_reinit:] = init_population(n_reinit, NUM_VEHICLES, DESTINATIONS)

        population = new_pop
        if gen % 50 == 0 or gen == 1:
            print(f"Gen {gen}: mejor fitness = {best_fit:.2f}")

    # Reporte final
    total_distance = sum(fitness([route]) for route in best_solution)
    print("Mejor solución:", best_solution)
    print(f"Distancia total: {total_distance:.2f}")

if __name__ == "__main__":
    genetic_vrp()
