import random
import math

def orderCrossover(parent1, parent2):
    """Order Crossover (OX)"""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    child1 = [-1] * size
    child2 = [-1] * size
    
    # Copiar segmento
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]
    
    # Preencher restante
    def fillChild(child, otherParent):
        used = set(child[start:end])
        pos = end
        for gene in otherParent[end:] + otherParent[:end]:
            if gene not in used:
                child[pos % size] = gene
                pos += 1
    
    fillChild(child1, parent2)
    fillChild(child2, parent1)
    
    return child1, child2

def pmxCrossover(parent1, parent2):
    """Partially Mapped Crossover (PMX)"""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    child1 = parent1[:]
    child2 = parent2[:]
    
    # Mapear segmento
    for i in range(start, end):
        val1, val2 = child1[i], child2[i]
        child1[i], child2[i] = val2, val1
        
        # Resolver conflitos
        idx1 = child1.index(val2) if val2 in child1[:i] + child1[i+1:] else -1
        idx2 = child2.index(val1) if val1 in child2[:i] + child2[i+1:] else -1
        
        if idx1 != -1:
            child1[idx1] = val1
        if idx2 != -1:
            child2[idx2] = val2
    
    return child1, child2

def cycleCrossover(parent1, parent2):
    """Cycle Crossover (CX)"""
    size = len(parent1)
    child1 = [-1] * size
    child2 = [-1] * size
    
    visited = [False] * size
    
    for start in range(size):
        if visited[start]:
            continue
            
        # Encontrar ciclo
        cycle = []
        current = start
        while not visited[current]:
            visited[current] = True
            cycle.append(current)
            current = parent1.index(parent2[current])
        
        # Alternar pais para cada ciclo
        if len([i for i in range(start) if not visited[i]]) % 2 == 0:
            for pos in cycle:
                child1[pos] = parent1[pos]
                child2[pos] = parent2[pos]
        else:
            for pos in cycle:
                child1[pos] = parent2[pos]
                child2[pos] = parent1[pos]
    
    return child1, child2

def uniformCrossover(parent1, parent2):
    """Uniform Crossover (UX)"""
    size = len(parent1)
    child1 = []
    child2 = []
    used1 = set()
    used2 = set()
    
    # Primeira passada - genes únicos
    for i in range(size):
        if random.random() < 0.5:
            if parent1[i] not in used1:
                child1.append(parent1[i])
                used1.add(parent1[i])
            if parent2[i] not in used2:
                child2.append(parent2[i])
                used2.add(parent2[i])
        else:
            if parent2[i] not in used1:
                child1.append(parent2[i])
                used1.add(parent2[i])
            if parent1[i] not in used2:
                child2.append(parent1[i])
                used2.add(parent1[i])
    
    # Completar com genes faltantes
    allGenes = set(parent1)
    for gene in parent1:
        if gene not in used1:
            child1.append(gene)
        if gene not in used2:
            child2.append(gene)
    
    return child1, child2

def srexCrossover(parent1, parent2):
    """Selective Route Exchange (SREX)"""
    size = len(parent1)
    # Selecionar segmento aleatório
    start = random.randint(0, size-2)
    end = random.randint(start+1, size)
    
    child1 = parent1[:]
    child2 = parent2[:]
    
    # Trocar segmentos
    segment1 = parent1[start:end]
    segment2 = parent2[start:end]
    
    # Remover elementos do segmento trocado
    for gene in segment2:
        if gene in child1:
            child1.remove(gene)
    for gene in segment1:
        if gene in child2:
            child2.remove(gene)
    
    # Inserir segmentos
    child1[start:start] = segment2
    child2[start:start] = segment1
    
    return child1[:size], child2[:size]

def smcCrossover(parent1, parent2):
    """Sinusoidal Motion Crossover (SMC)"""
    size = len(parent1)
    child1 = []
    child2 = []
    used1 = set()
    used2 = set()
    
    for i in range(size):
        # Função sinusoidal para determinar seleção
        prob = (math.sin(2 * math.pi * i / size) + 1) / 2
        
        if random.random() < prob:
            if parent1[i] not in used1:
                child1.append(parent1[i])
                used1.add(parent1[i])
            if parent2[i] not in used2:
                child2.append(parent2[i])
                used2.add(parent2[i])
        else:
            if parent2[i] not in used1:
                child1.append(parent2[i])
                used1.add(parent2[i])
            if parent1[i] not in used2:
                child2.append(parent1[i])
                used2.add(parent1[i])
    
    # Completar genes faltantes
    allGenes = set(parent1)
    for gene in parent1:
        if gene not in used1:
            child1.append(gene)
        if gene not in used2:
            child2.append(gene)
    
    return child1, child2

# Dicionário de operadores
crossoverOperators = {
    'OX': orderCrossover,
    'PMX': pmxCrossover,
    'CX': cycleCrossover,
    'UX': uniformCrossover,
    'SREX': srexCrossover,
    'SMC': smcCrossover
}