import googlemaps
import pandas as pd
import numpy as np
import time

# Configuração da API
API_KEY = "AIzaSyD5uHIIYrwmkFHL9U8n5qO1DH0QIN6Q2MA"  # Substitua pela sua chave da API do Google Maps
gmaps = googlemaps.Client(key=API_KEY)

def createDistanceMatrix(addresses):
    """Cria matriz de distâncias usando Google Maps API"""
    n = len(addresses)
    distanceMatrix = np.zeros((n, n))
    
    print(f"Processando {n} endereços...")
    
    # Processar em lotes para evitar limite da API
    batchSize = 10
    totalBatches = ((n - 1) // batchSize + 1) ** 2
    currentBatch = 0
    
    for i in range(0, n, batchSize):
        for j in range(0, n, batchSize):
            currentBatch += 1
            origins = addresses[i:i+batchSize]
            destinations = addresses[j:j+batchSize]
            
            print(f"Processando lote {currentBatch}/{totalBatches} - Origens {i}-{min(i+batchSize-1, n-1)}, Destinos {j}-{min(j+batchSize-1, n-1)}")
            
            try:
                # Chamada para API
                result = gmaps.distance_matrix(
                    origins=origins,
                    destinations=destinations,
                    mode="driving",
                    units="metric",
                    avoid="tolls"
                )
                
                # Extrair distâncias
                for oi, origin_result in enumerate(result['rows']):
                    for di, dest_result in enumerate(origin_result['elements']):
                        if dest_result['status'] == 'OK':
                            distance = dest_result['distance']['value'] / 1000  # Converter para km
                            distanceMatrix[i+oi][j+di] = distance
                        else:
                            print(f"Erro para rota {i+oi} -> {j+di}: {dest_result['status']}")
                            distanceMatrix[i+oi][j+di] = float('inf')
                
                # Delay para respeitar limites da API
                time.sleep(0.2)
                
            except Exception as e:
                print(f"Erro no lote {i}-{j}: {e}")
                # Preencher com valores altos em caso de erro
                for oi in range(len(origins)):
                    for di in range(len(destinations)):
                        if i+oi < n and j+di < n:
                            distanceMatrix[i+oi][j+di] = 9999
    
    return distanceMatrix

def loadAddressesFromFile(filename, column_name='endereco'):
    """Carrega endereços de uma planilha (Excel ou ODS)"""
    try:
        if filename.endswith('.ods'):
            df = pd.read_excel(filename, engine='odf', header=None)
        else:
            df = pd.read_excel(filename)
        
        print(f"Formato da planilha: {df.shape}")
        print(f"Primeiras linhas:")
        print(df.head())
        
        # Se não tem cabeçalho, usar primeira coluna ou linha
        if column_name.isdigit():
            col_idx = int(column_name)
            addresses = df.iloc[:, col_idx].dropna().tolist()
        elif column_name.upper() in ['A', 'B', 'C', 'D', 'E']:
            col_idx = ord(column_name.upper()) - ord('A')
            addresses = df.iloc[:, col_idx].dropna().tolist()
        else:
            # Tentar usar como nome de coluna
            addresses = df[column_name].dropna().tolist()
        
        print(f"Carregados {len(addresses)} endereços da planilha")
        return addresses
    except Exception as e:
        print(f"Erro ao carregar planilha: {e}")
        return []

def saveDistanceMatrix(distMatrix, addresses, filename_prefix="matriz_distancias"):
    """Salva a matriz de distâncias em diferentes formatos"""
    # Salvar como CSV
    np.savetxt(f"{filename_prefix}.csv", distMatrix, delimiter=",", fmt='%.2f')
    
    # Salvar como Excel com nomes dos endereços
    df = pd.DataFrame(distMatrix, index=addresses, columns=addresses)
    df.to_excel(f"{filename_prefix}.xlsx")
    
    # Salvar como array Python para usar no código VRP
    with open(f"{filename_prefix}.py", 'w') as f:
        f.write("# Matriz de distâncias gerada automaticamente\n")
        f.write("distanceMatrix = [\n")
        for row in distMatrix:
            f.write("    [" + ", ".join([f"{val:.0f}" for val in row]) + "],\n")
        f.write("]\n")
    
    print(f"Matriz salva em: {filename_prefix}.csv, {filename_prefix}.xlsx, {filename_prefix}.py")

def main():
    print("=== GERADOR DE MATRIZ DE DISTÂNCIAS ===")
    
    # Configurações
    excel_file = input("Nome do arquivo (ex: DistanciasCompev.ods): ")
    column_name = input("Coluna com endereços (A, B, C... ou número 0, 1, 2...): ") or "A"
    
    # Carregar endereços
    addresses = loadAddressesFromFile(excel_file, column_name)
    
    if not addresses:
        print("Nenhum endereço encontrado!")
        return
    
    print("\nEndereços carregados:")
    for i, addr in enumerate(addresses):
        print(f"{i}: {addr}")
    
    confirm = input(f"\nProcessar {len(addresses)} endereços? (s/n): ")
    if confirm.lower() != 's':
        return
    
    # Gerar matriz de distâncias
    print("\nIniciando geração da matriz...")
    distMatrix = createDistanceMatrix(addresses)
    
    # Salvar resultados
    output_name = input("Nome dos arquivos de saída (padrão: matriz_distancias): ") or "matriz_distancias"
    saveDistanceMatrix(distMatrix, addresses, output_name)
    
    print("\n=== CONCLUÍDO ===")
    print(f"Matriz {len(addresses)}x{len(addresses)} gerada com sucesso!")
    
    # Mostrar estatísticas
    valid_distances = distMatrix[distMatrix != float('inf')]
    if len(valid_distances) > 0:
        print(f"Distância mínima: {valid_distances.min():.2f} km")
        print(f"Distância máxima: {valid_distances.max():.2f} km")
        print(f"Distância média: {valid_distances.mean():.2f} km")

if __name__ == "__main__":
    main()