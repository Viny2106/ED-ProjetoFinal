"""
atribuicoes_diretor.py
Interface entre o main.py e a ÁRVORE BINÁRIA DE BUSCA (Seção 3.2).

Antes de qualquer operação do diretor, a árvore é gerada a partir da
lista encadeada do secretário (função preparar_arvore).
"""

import atribuicoes_secretario
from arvore_binaria import gerar_arvore_da_lista

_arvore = None


def preparar_arvore():
    """Gera a ABB a partir da lista encadeada (chave = nome)."""
    global _arvore
    _arvore = gerar_arvore_da_lista(atribuicoes_secretario.obter_lista_espera())


def consultar_pessoa(nome):
    pessoa = _arvore.buscar(nome)
    return str(pessoa) if pessoa else None


def nome_ja_cadastrado(nome):
    return _arvore.buscar(nome) is not None


# ----------------------------------------------------------- Opção 1: editar
def alterar_nome(nome_atual, novo_nome):
    """
    O nome é a CHAVE da árvore. Mudar a chave "no lugar" quebraria a regra
    da ABB, por isso: remove o nó, altera o nome e reinsere na posição certa.
    """
    pessoa = _arvore.remover(nome_atual)
    if pessoa is None:
        return None
    pessoa.nome = novo_nome
    _arvore.inserir(pessoa)
    return str(pessoa)


def alterar_idade(nome, nova_idade):
    pessoa = _arvore.buscar(nome)
    if pessoa is None:
        return None
    pessoa.idade = nova_idade     # idade não é chave: altera direto
    return str(pessoa)


def alterar_telefone(nome, novo_telefone):
    pessoa = _arvore.buscar(nome)
    if pessoa is None:
        return None
    pessoa.telefone = novo_telefone
    return str(pessoa)


# -------------------------------------------------------- Opção 2: remover
def descadastrar_pessoa(nome):
    return _arvore.remover(nome) is not None


# -------------------------------------------------- Opções 3 e 4: mín/máx
def primeira_pessoa_alfabetica():
    pessoa = _arvore.minimo()
    return str(pessoa) if pessoa else None


def ultima_pessoa_alfabetica():
    pessoa = _arvore.maximo()
    return str(pessoa) if pessoa else None


def obter_arvore():
    """Usado pelo atribuicoes_assistente (não pelo main)."""
    return _arvore
