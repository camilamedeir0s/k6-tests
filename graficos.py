import json
import os
import matplotlib.pyplot as plt
import numpy as np
import re

# Configurações iniciais
results_dir = "./results-26-12-24"  # Pasta onde estão os arquivos JSON
output_graph = "test_results_grouped_bar_chart_spaced_color_26-12-24.png"  # Nome do arquivo do gráfico gerado

# Carregar dados
data = {}
for filename in os.listdir(results_dir):
    if filename.endswith(".json"):
        # config_name = filename.split(".", 1)[0]  # Extrair "colocated", "monolitico", etc.
        config_name = re.sub(r'_\d+\.json$', '', filename)
        with open(os.path.join(results_dir, filename), 'r') as file:
            json_data = json.load(file)
            #vu = json_data["metrics"]["iterations"]["values"]["count"]
            vu = json_data["metrics"]["vus_max"]["values"]["value"]
            p95 = json_data["metrics"]["iteration_duration"]["values"]["p(95)"]
            if vu not in data:
                data[vu] = {}
            data[vu][config_name] = p95

# Ordenar dados para consistência
sorted_vus = sorted(data.keys())  # Número de usuários ordenados
configs = sorted({config for vu_data in data.values() for config in vu_data})  # Todas as configurações

# Criar matriz de dados para o gráfico
values_matrix = []
for vu in sorted_vus:
    row = [data[vu].get(config, 0) for config in configs]
    values_matrix.append(row)
values_matrix = np.array(values_matrix)

# Criar gráfico com espaçamento entre grupos
group_spacing = 2  # Espaçamento entre grupos de barras
x = np.arange(len(sorted_vus)) * group_spacing  # Posições no eixo X para os grupos
bar_width = 0.1  # Barras mais finas
plt.figure(figsize=(14, 8))

# Gerar paleta com 15 cores distintas
num_configs = len(configs)
cmap = plt.colormaps.get_cmap("tab20")
colors = [cmap(i) for i in np.linspace(0, 1, num_configs)]

# Adicionar barras para cada configuração
for i, config in enumerate(configs):
    positions = x + i * bar_width
    plt.bar(positions, values_matrix[:, i], bar_width, label=config, color=colors[i])

# Configurações do gráfico
plt.xlabel("Número de Usuários")
plt.ylabel("Tempo de Resposta Percentil 95 (ms)")
plt.title("Resultados de Testes de Carga")
plt.xticks(x + (len(configs) - 1) * bar_width / 2, sorted_vus)  # Centralizar rótulos no grupo
plt.legend(title="Configuração")
plt.tight_layout()

# Salvar e mostrar gráfico
plt.savefig(output_graph)
plt.show()
