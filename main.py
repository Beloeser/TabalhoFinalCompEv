import random
import math
from crossover import crossoverOperators
from mutacao import mutationOperators

# CONFIG VRP
numPoints = 10
startIdx = 0
numVehicles = 3       
generations = 100
popSize = 50
crossoverRate = 0.9
mutationRate = 0.05

def generateDistanceMatrix():
    distKm = [
        [0, 123, 234, 345, 456, 567, 678, 789, 890, 901],
        [123, 0, 210, 320, 430, 540, 650, 760, 870, 980],
        [234, 210, 0, 150, 260, 370, 480, 590, 700, 810],
        [345, 320, 150, 0, 110, 220, 330, 440, 550, 660],
        [456, 430, 260, 110, 0, 130, 240, 350, 460, 570],
        [567, 540, 370, 220, 130, 0, 150, 260, 370, 480],
        [678, 650, 480, 330, 240, 150, 0, 110, 220, 330],
        [789, 760, 590, 440, 350, 260, 110, 0, 130, 240],
        [890, 870, 700, 550, 460, 370, 220, 130, 0, 110],
        [901, 980, 810, 660, 570, 480, 330, 240, 110, 0],
    ]
    return distKm



def splitIntoVehicles(route):
    """Divide a rota única em rotas menores para vários veículos"""
    chunkSize = math.ceil(len(route) / numVehicles)
    return [route[i:i+chunkSize] for i in range(0, len(route), chunkSize)]



def fitnessVRP(route, distMatrix):
    """Calcula o custo total das rotas dos veículos"""
    total = 0
    routes = splitIntoVehicles(route)

    for r in routes:
        current = 0  # depósito
        for c in r:
            total += distMatrix[current][c]
            current = c
        total += distMatrix[current][0]  # volta ao depósito

    return total


def createInitialPopulation():
    population = []
    baseRoute = list(range(1, numPoints))

    for _ in range(popSize):
        r = baseRoute[:]
        random.shuffle(r)
        population.append(r)

    return population


def selectParents(population, dist):
    k = 3
    sample = random.sample(population, k)
    return min(sample, key=lambda r: fitnessVRP(r, dist))


def geneticAlgorithm(distMatrix):
    print("OPERADORES DE CROSSOVER:")
    for i, op in enumerate(crossoverOperators.keys(), 1):
        print(f"{i}. {op}")
    crossChoice = int(input("Escolha: ")) - 1
    crossover = list(crossoverOperators.values())[crossChoice]

    print("\nOPERADORES DE MUTAÇÃO:")
    for i, op in enumerate(mutationOperators.keys(), 1):
        print(f"{i}. {op}")
    mutChoice = int(input("Escolha: ")) - 1
    mutate = list(mutationOperators.values())[mutChoice]

    population = createInitialPopulation()
    best = min(population, key=lambda r: fitnessVRP(r, distMatrix))
    bestFit = fitnessVRP(best, distMatrix)

    for gen in range(generations):
        newPop = [best[:]]

        while len(newPop) < popSize:
            p1 = selectParents(population, distMatrix)
            p2 = selectParents(population, distMatrix)

            if random.random() < crossoverRate:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]

            if random.random() < mutationRate:
                c1 = mutate(c1)
            if random.random() < mutationRate:
                c2 = mutate(c2)

            newPop.extend([c1, c2])

        population = newPop[:popSize]

        current = min(population, key=lambda r: fitnessVRP(r, distMatrix))
        currentFit = fitnessVRP(current, distMatrix)

        if currentFit < bestFit:
            best = current[:]
            bestFit = currentFit
            print(f"Geração {gen+1}: NOVO MELHOR = {bestFit}")

    return best, bestFit


def printVRP(route, distMatrix):
    routes = splitIntoVehicles(route)
    print("\n==== MELHORES ROTAS POR VEÍCULO ====")

    for i, r in enumerate(routes):
        print(f"\nVeículo {i+1}: 0 -> {' -> '.join(map(str,r))} -> 0")
        curr = 0
        dist = 0
        for c in r:
            dist += distMatrix[curr][c]
            curr = c
        dist += distMatrix[curr][0]
        print(f"Distância: {dist} km")



def main():
    print("=== VRP - ROTEAMENTO DE VEÍCULOS ===")
    print(f"Clientes: {numPoints-1}")
    print(f"Veículos: {numVehicles}")

    dist = generateDistanceMatrix()
    best, bestFit = geneticAlgorithm(dist)

    printVRP(best, dist)
    print(f"\nCusto total: {bestFit} km")


if __name__ == "__main__":
    main()
