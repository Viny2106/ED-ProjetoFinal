"""
lista_encadeada.py
Lista encadeada simples usada pelo(a) secretário(a).

Cada nó guarda uma Pessoa e uma referência para o próximo nó.
    cabeca -> [João] -> [Maria] -> [Paulo] -> None
"""


class No:
    def __init__(self, pessoa):
        self.pessoa = pessoa
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.cabeca = None      # primeiro nó
        self.cauda = None       # último nó (permite inserir no fim em O(1))
        self.tamanho = 0        # contador (quantidade em O(1))

    def inserir(self, pessoa):
        """Insere a pessoa no FIM da lista (ordem de chegada)."""
        novo = No(pessoa)
        if self.cabeca is None:          # lista vazia
            self.cabeca = novo
            self.cauda = novo
        else:
            self.cauda.proximo = novo
            self.cauda = novo
        self.tamanho += 1

    def buscar(self, nome):
        """Busca sequencial pelo nome. Retorna a Pessoa ou None. O(n)."""
        atual = self.cabeca
        while atual is not None:
            if atual.pessoa.nome == nome:
                return atual.pessoa
            atual = atual.proximo
        return None

    def quantidade(self):
        return self.tamanho

    def esta_vazia(self):
        return self.cabeca is None

    def __iter__(self):
        """Permite percorrer a lista com 'for pessoa in lista'."""
        atual = self.cabeca
        while atual is not None:
            yield atual.pessoa
            atual = atual.proximo

    def __str__(self):
        return "\n".join(str(p) for p in self)
