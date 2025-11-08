import random

def inversionMutation(route):
    """Inversion Mutation """
    route = route[:]
    if len(route) < 2:
        return route
    
    start, end = sorted(random.sample(range(len(route)), 2))
    route[start:end+1] = reversed(route[start:end+1])
    return route

def swapMutation(route):
    """Swap Mutation"""
    route = route[:]
    if len(route) < 2:
        return route
    
    i, j = random.sample(range(len(route)), 2)
    route[i], route[j] = route[j], route[i]
    return route

def combinationSwapInversion(route):
    """Combination Swap + Inversion"""
    route = swapMutation(route)
    route = inversionMutation(route)
    return route

def moveTwoClientsReversed(route):
    """MoveTwoClientsReversed """
    route = route[:]
    if len(route) < 3:
        return route
    
    # Selecionar dois clientes adjacentes
    start = random.randint(0, len(route)-2)
    clients = route[start:start+2]
    
    # Remover clientes
    del route[start:start+2]
    
    # Inserir em nova posição (invertidos)
    newPos = random.randint(0, len(route))
    route[newPos:newPos] = reversed(clients)
    
    return route

#ver como que colocaria o 2 opt
    """2-OPT """
    
    
    # Inverter segmento entre i+1 e j
    route[i+1:j+1] = reversed(route[i+1:j+1])
    return route

def relocateMutation(route):
    """RELOCATE """
    route = route[:]
    if len(route) < 2:
        return route
    
    # Selecionar cliente para mover
    oldPos = random.randint(0, len(route)-1)
    client = route.pop(oldPos)
    
    # Nova posição
    newPos = random.randint(0, len(route))
    route.insert(newPos, client)
    
    return route

def swapAdvancedMutation(route):
    """SWAP"""
    route = route[:]
    if len(route) < 4:
        return route
    
    # Selecionar dois segmentos não sobrepostos
    seg1Start = random.randint(0, len(route)//2-1)
    seg1End = random.randint(seg1Start+1, len(route)//2)
    
    seg2Start = random.randint(len(route)//2, len(route)-2)
    seg2End = random.randint(seg2Start+1, len(route))
    
    # Trocar segmentos
    segment1 = route[seg1Start:seg1End]
    segment2 = route[seg2Start:seg2End]
    
    newRoute = route[:seg1Start] + segment2 + route[seg1End:seg2Start] + segment1 + route[seg2End:]
    
    return newRoute

# Dicionário de operadores
mutationOperators = {
    'INVERSION': inversionMutation,
    'SWAP': swapMutation,
    'COMBINATION': combinationSwapInversion,
    'MOVE_TWO': moveTwoClientsReversed,
    #'2OPT': twoOptMutation,
    'RELOCATE': relocateMutation,
    'SWAP_ADV': swapAdvancedMutation
}