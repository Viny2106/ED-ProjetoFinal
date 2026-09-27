"""
atribuicoes_secretario.py
Interface entre o main.py e a LISTA ENCADEADA SIMPLES (Seção 3.1).

O main.py nunca acessa a lista diretamente: ele chama as funções abaixo,
que devolvem apenas textos/valores prontos para exibir.
"""

import os
import random

from pessoa import Pessoa
from lista_encadeada import ListaEncadeada
from grafo import listar_cidades_do_arquivo

ARQUIVO_CIDADES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "cidades_vizinhas.csv")

# Estado do módulo: a lista de espera (em memória principal)
_lista_espera = ListaEncadeada()
_cidades = listar_cidades_do_arquivo(ARQUIVO_CIDADES)


def nome_ja_cadastrado(nome):
    return _lista_espera.buscar(nome) is not None


def cadastrar_pessoa(nome, idade, telefone):
    """Opção 1: cria a pessoa com cidade aleatória e insere na lista.
    Retorna o texto da lista completa após a inclusão."""
    cidade = random.choice(_cidades)
    _lista_espera.inserir(Pessoa(nome, idade, telefone, cidade))
    return str(_lista_espera)


def consultar_pessoa(nome):
    """Opção 2: retorna o texto com os dados da pessoa ou None."""
    pessoa = _lista_espera.buscar(nome)
    return str(pessoa) if pessoa else None


def quantidade_pessoas():
    """Opção 3."""
    return _lista_espera.quantidade()


def obter_lista_espera():
    """Usado pelo atribuicoes_diretor para gerar a árvore (não pelo main)."""
    return _lista_espera
