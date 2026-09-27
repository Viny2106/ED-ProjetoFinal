"""
atribuicoes_assistente.py
Interface entre o main.py e o GRAFO de cidades (Seção 3.3).

As pessoas são encontradas na árvore validada pelo diretor (que é a
lista de espera final) e as distâncias vêm do grafo (Dijkstra).
"""

import atribuicoes_diretor
from grafo import carregar_grafo
from atribuicoes_secretario import ARQUIVO_CIDADES

CIDADE_ESCOLA = "Guarujá"
CIDADE_INTERMEDIARIA = "Indaiatuba"

_grafo = carregar_grafo(ARQUIVO_CIDADES)


def _buscar(nome):
    arvore = atribuicoes_diretor.obter_arvore()
    return arvore.buscar(nome) if arvore else None


def _formatar(caminho, custo):
    if caminho is None:
        return "Não existe caminho entre as cidades informadas."
    return f"Menor caminho = {caminho} com custo {custo}"


def menor_caminho_ate_pessoa(nome):
    """Opção 1: retorna (texto_da_pessoa, texto_do_caminho) ou None."""
    pessoa = _buscar(nome)
    if pessoa is None:
        return None
    caminho, custo = _grafo.menor_caminho(CIDADE_ESCOLA, pessoa.cidade)
    return str(pessoa), _formatar(caminho, custo)


def menor_caminho_via_intermediaria(nome):
    """Opção 2: Guarujá -> Indaiatuba -> cidade da pessoa."""
    pessoa = _buscar(nome)
    if pessoa is None:
        return None
    caminho, custo = _grafo.menor_caminho_passando_por(
        CIDADE_ESCOLA, CIDADE_INTERMEDIARIA, pessoa.cidade)
    return str(pessoa), _formatar(caminho, custo)


def moradores_cidade_mais_proxima():
    """
    Opção 3: um único Dijkstra a partir da escola dá a distância para
    todas as cidades; entre as cidades que têm moradores na lista de
    espera, escolhe a de menor distância.
    Retorna (cidade, distancia, [textos das pessoas]) ou None.
    """
    arvore = atribuicoes_diretor.obter_arvore()
    pessoas = arvore.em_ordem() if arvore else []
    if not pessoas:
        return None

    distancias, _ = _grafo.dijkstra(CIDADE_ESCOLA)
    cidade_mais_proxima = min({p.cidade for p in pessoas},
                              key=lambda c: distancias.get(c, float("inf")))
    distancia = distancias.get(cidade_mais_proxima, float("inf"))
    moradores = [str(p) for p in pessoas if p.cidade == cidade_mais_proxima]
    return cidade_mais_proxima, distancia, moradores
