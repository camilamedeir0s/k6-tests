import json
import os
import re

# Configurações iniciais
results_dir = "./results-25-01-21-VUs50-200"  # Pasta onde estão os arquivos JSON
output_dir = "./percentis_95_ordenados"  # Pasta para salvar os arquivos TXT

# Criar diretório de saída, se não existir
os.makedirs(output_dir, exist_ok=True)

# Dicionário para armazenar os percentis 95 por VU
data = {}

# Percorrer os arquivos JSON na pasta
for filename in os.listdir(results_dir):
    if filename.endswith(".json"):
        config_name = re.sub(r'_\d+\.json$', '', filename)  # Extrai o nome da configuração
        with open(os.path.join(results_dir, filename), 'r') as file:
            json_data = json.load(file)
            vu = json_data["metrics"]["vus_max"]["values"]["value"]  # Número máximo de VUs
            p95 = json_data["metrics"]["iteration_duration"]["values"]["p(95)"]  # Percentil 95

            if vu not in data:
                data[vu] = []
            data[vu].append((config_name, p95))

# Lista de VUs desejados
vus_desejados = [50, 100, 150, 200]

# Criar arquivos TXT para cada VU desejado
for vu in vus_desejados:
    if vu in data:
        sorted_configs = sorted(data[vu], key=lambda x: x[1])  # Ordena pelo percentil 95
        output_file = os.path.join(output_dir, f"percentis95_VUs{vu}.txt")
        
        with open(output_file, "w") as f:
            for config_name, p95 in sorted_configs:
                f.write(f"{config_name}: {p95} ms\n")

print(f"Arquivos TXT gerados em {output_dir}")
