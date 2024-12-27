import json
import os
import matplotlib.pyplot as plt
import numpy as np
import re

# Configurações iniciais
results_dir = "./results-26-12-24"  # Pasta onde estão os arquivos JSON
output_graph = "test_results_graph_adjusted_no_overlap_26-12-24.png"  # Nome do arquivo do gráfico gerado

# Gerar paleta com 15 cores distintas
colors = plt.cm.get_cmap("tab20", 15)  # Usar "tab20" para obter até 20 cores distintas

# Carregar dados
data = {}
for filename in os.listdir(results_dir):
    if filename.endswith(".json"):
        #config_name = filename.split(".", 1)[0]  # Extrair "colocated", "monolitico", etc.
        config_name = re.sub(r'_\d+\.json$', '', filename)
        with open(os.path.join(results_dir, filename), 'r') as file:
            json_data = json.load(file)
            vu = json_data["metrics"]["vus_max"]["values"]["value"]
            p95 = json_data["metrics"]["iteration_duration"]["values"]["p(95)"]
            if config_name not in data:
                data[config_name] = []
            data[config_name].append((vu, p95))

# Ordenar os dados para consistência no gráfico
for config in data:
    data[config].sort()

# Preparar posições para evitar sobreposição
total_bars = sum(len(values) for values in data.values())  # Total de barras no gráfico
bar_width = 0.2  # Largura das barras
gap = 0.3  # Espaçamento entre grupos de barras
positions = np.arange(total_bars) * (bar_width + gap)  # Posição espaçada no eixo X

# Criar gráfico
plt.figure(figsize=(12, 7))

# Plotar cada barra
current_position = 0
for i, (config, values) in enumerate(data.items()):
    vus = [v[0] for v in values]
    p95s = [v[1] for v in values]
    print(colors(i))
    plt.bar(positions[current_position:current_position + len(vus)], p95s, bar_width, label=config, color=colors(i))
    current_position += len(vus)

# Configurações do gráfico
plt.xlabel("Número de VUs")
plt.ylabel("Percentil 95 da Duração (ms)")
plt.title("Resultados de Testes de Carga ~2min de duração para cada teste")
plt.xticks(
    positions[:current_position] + bar_width / 2,  # Centralizar labels no grupo
    #[f"{v[0]} ({config})" for config, values in data.items() for v in values],  # Labels detalhados por configuração
    [f"{v[0]}" for config, values in data.items() for v in values],  # Labels detalhados por configuração
    rotation=45,
    ha="right"
)
plt.legend(title="Configuração", loc="upper left", bbox_to_anchor=(1, 1))  # Legenda ajustada fora do gráfico
plt.tight_layout()

# Salvar gráfico
plt.savefig(output_graph)
plt.show()
