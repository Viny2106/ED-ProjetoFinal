"""
grafo.py
Grafo ponderado e NÃO-direcionado criado a partir de cidades_vizinhas.csv.

Representação: lista de adjacência (dicionário de dicionários)
    adjacencias["Santos"] = {"Guarujá": 10, "São Paulo": 77, ...}

Como o grafo é não-direcionado, cada linha "A,B,d" do CSV gera
as duas arestas A->B e B->A com o mesmo peso d.

Menor caminho: algoritmo de Dijkstra (pesos são distâncias >= 0).
"""

import csv
import heapq


class Grafo:
    def __init__(self):
        self.adjacencias = {}

    def adicionar_aresta(self, a, b, peso):
        self.adjacencias.setdefault(a, {})
        self.adjacencias.setdefault(b, {})
        # Se houver aresta repetida, fica a menor distância
        if b not in self.adjacencias[a] or peso < self.adjacencias[a][b]:
            self.adjacencias[a][b] = peso
            self.adjacencias[b][a] = peso

    def cidades(self):
        return list(self.adjacencias.keys())

    def existe_cidade(self, cidade):
        return cidade in self.adjacencias

    # ------------------------------------------------------------ Dijkstra
    def dijkstra(self, origem):
        """
        Calcula a menor distância da 'origem' para TODAS as cidades.
        Retorna (distancias, anteriores):
            distancias[c] = menor custo origem -> c
            anteriores[c] = cidade que vem antes de c no menor caminho
        """
        distancias = {c: float("inf") for c in self.adjacencias}
        anteriores = {c: None for c in self.adjacencias}
        distancias[origem] = 0
        fila = [(0, origem)]                # fila de prioridade (heap)
        visitados = set()

        while fila:
            dist_atual, cidade = heapq.heappop(fila)
            if cidade in visitados:
                continue
            visitados.add(cidade)
            for vizinha, peso in self.adjacencias[cidade].items():
                nova_dist = dist_atual + peso
                if nova_dist < distancias[vizinha]:     # relaxamento
                    distancias[vizinha] = nova_dist
                    anteriores[vizinha] = cidade
                    heapq.heappush(fila, (nova_dist, vizinha))
        return distancias, anteriores

    def menor_caminho(self, origem, destino):
        """Retorna (lista_de_cidades, custo) ou (None, inf) se não houver."""
        if not (self.existe_cidade(origem) and self.existe_cidade(destino)):
            return None, float("inf")
        distancias, anteriores = self.dijkstra(origem)
        if distancias[destino] == float("inf"):
            return None, float("inf")
        # Reconstrói o caminho andando de trás para frente
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]
        caminho.reverse()
        return caminho, distancias[destino]

    def menor_caminho_passando_por(self, origem, intermediaria, destino):
        """
        Menor caminho origem -> intermediária -> destino.
        É a junção de dois Dijkstra: (origem -> intermediária) e
        (intermediária -> destino). A intermediária não é repetida na junção.
        """
        caminho1, custo1 = self.menor_caminho(origem, intermediaria)
        caminho2, custo2 = self.menor_caminho(intermediaria, destino)
        if caminho1 is None or caminho2 is None:
            return None, float("inf")
        return caminho1 + caminho2[1:], custo1 + custo2


def _ler_linhas_csv(caminho_arquivo):
    """Lê o CSV aceitando ',' ou ';' e codificação UTF-8 ou Latin-1."""
    for codificacao in ("utf-8-sig", "latin-1"):
        try:
            with open(caminho_arquivo, encoding=codificacao) as f:
                conteudo = f.read()
            break
        except UnicodeDecodeError:
            continue
    separador = ";" if conteudo.count(";") > conteudo.count(",") else ","
    return list(csv.reader(conteudo.splitlines(), delimiter=separador))


def listar_cidades_do_arquivo(caminho_arquivo):
    """Todas as cidades (sem repetição) das duas primeiras colunas do CSV."""
    cidades = set()
    for linha in _ler_linhas_csv(caminho_arquivo):
        if len(linha) >= 2:
            cidades.add(linha[0].strip())
            cidades.add(linha[1].strip())
    return sorted(cidades)


def carregar_grafo(caminho_arquivo):
    """Cria o grafo a partir do CSV (cidade1, cidade2, distância)."""
    grafo = Grafo()
    for linha in _ler_linhas_csv(caminho_arquivo):
        if len(linha) < 3:
            continue
        cidade1, cidade2, distancia = linha[0].strip(), linha[1].strip(), linha[2].strip()
        try:
            peso = float(distancia.replace(",", "."))
        except ValueError:
            continue            # ignora cabeçalho, se existir
        if peso.is_integer():
            peso = int(peso)
        grafo.adicionar_aresta(cidade1, cidade2, peso)
    return grafo
