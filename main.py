import random
import math
from crossover import crossoverOperators
from mutacao import mutationOperators

# Configuração do problema
numPoints = 10 # mudar quando 
startIdx = 0
generations = 100
popSize = 50
crossoverRate = 0.9
mutationRate = 0.05

def generateDistanceMatrix(): #Colocar aqui depois a matriz com dados do wazw
    """Matriz de distâncias """
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

def createInitialPopulation():
    """Cria população inicial de rotas aleatórias"""
    population = []
    baseRoute = list(range(1, numPoints)) 
    
    for _ in range(popSize):
        route = baseRoute[:]
        random.shuffle(route)
        population.append(route)
    
    return population

def fitnessFunction(route, distMatrix):
    """Calcula aptidão da rota (distância total)"""
    totalDistance = 0
    current = startIdx
    
    # Percorrer todos os pontos da rota
    for point in route:
        totalDistance += distMatrix[current][point]
        current = point
    
    # Retornar ao ponto inicial
    totalDistance += distMatrix[current][startIdx]
    
    return totalDistance

def printRouteInfo(route, distMatrix, label="Rota"):
    """Imprime informações da rota"""
    fitness = fitnessFunction(route, distMatrix)
    routeStr = f"0 -> {' -> '.join(map(str, route))} -> 0"
    print(f"{label}: {routeStr}")
    print(f"Distância total: {fitness} km")
    print("-" * 50)

def selectParents(population, distMatrix):
    """Seleção por torneio"""
    tournamentSize = 3
    tournament = random.sample(population, tournamentSize)
    return min(tournament, key=lambda route: fitnessFunction(route, distMatrix))

def geneticAlgorithm(distMatrix):
    """Algoritmo Genético completo"""
    # Escolher operadores
    print("OPERADORES DE CROSSOVER DISPONÍVEIS:")
    for i, op in enumerate(crossoverOperators.keys(), 1):
        print(f"{i}. {op}")
    crossoverChoice = input("\nEscolha o operador de crossover (número): ")
    crossoverFunc = list(crossoverOperators.values())[int(crossoverChoice) - 1]
    
    print("\nOPERADORES DE MUTAÇÃO DISPONÍVEIS:")
    for i, op in enumerate(mutationOperators.keys(), 1):
        print(f"{i}. {op}")
    mutationChoice = input("\nEscolha o operador de mutação (número): ")
    mutationFunc = list(mutationOperators.values())[int(mutationChoice) - 1]
    
    # População inicial
    population = createInitialPopulation()
    bestRoute = min(population, key=lambda route: fitnessFunction(route, distMatrix))
    bestFitness = fitnessFunction(bestRoute, distMatrix)
    
    print(f"\n=== INICIANDO OTIMIZAÇÃO ({generations} gerações) ===")
    print(f"População inicial - Melhor fitness: {bestFitness} km")
    
    for generation in range(generations):
        newPopulation = []
        
        # Elitismo - manter melhor solução
        newPopulation.append(bestRoute[:])
        
        while len(newPopulation) < popSize:
            # Seleção
            parent1 = selectParents(population, distMatrix)
            parent2 = selectParents(population, distMatrix)
            
            # Crossover
            if random.random() < crossoverRate:
                child1, child2 = crossoverFunc(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]
            
            # Mutação
            if random.random() < mutationRate:
                child1 = mutationFunc(child1)
            if random.random() < mutationRate:
                child2 = mutationFunc(child2)
            
            newPopulation.extend([child1, child2])
        
        population = newPopulation[:popSize]
        
        # Atualizar melhor solução
        currentBest = min(population, key=lambda route: fitnessFunction(route, distMatrix))
        currentFitness = fitnessFunction(currentBest, distMatrix)
        
        if currentFitness < bestFitness:
            bestRoute = currentBest[:]
            bestFitness = currentFitness
            print(f"Geração {generation+1}: Nova melhor solução = {bestFitness} km")
        
        # Progresso a cada 10 gerações
        if (generation + 1) % 10 == 0:
            print(f"Geração {generation+1}: Melhor fitness = {bestFitness} km")
    
    return bestRoute, bestFitness

def main():
    print("=== PROBLEMA DE ROTEAMENTO DE VEÍCULOS (VRP) ===")
    print(f"Pontos: {numPoints} (nomeados de 0 a {numPoints-1})")
    print(f"Ponto inicial/final: {startIdx}")
    print()
    
    distMatrix = generateDistanceMatrix()
    
    # Executar algoritmo genético
    bestRoute, bestFitness = geneticAlgorithm(distMatrix)
    
    print("\n=== RESULTADO FINAL ===")
    printRouteInfo(bestRoute, distMatrix, "MELHOR ROTA ENCONTRADA")
    
    # Comparar com rota aleatória inicial
    randomRoute = list(range(1, numPoints))
    random.shuffle(randomRoute)
    randomFitness = fitnessFunction(randomRoute, distMatrix)
    
    improvement = randomFitness - bestFitness
    print(f"\nComparação com rota aleatória:")
    print(f"Rota aleatória: {randomFitness} km")
    print(f"Melhor rota AG: {bestFitness} km")
    print(f"Melhoria: {improvement} km ({improvement/randomFitness*100:.1f}%)")

if __name__ == "__main__":
    main()