"""
arvore_binaria.py
Árvore binária de busca (ABB) usada pelo(a) diretor(a).

Chave = nome da pessoa. Regra da ABB:
    tudo à ESQUERDA de um nó tem nome MENOR (ordem alfabética);
    tudo à DIREITA tem nome MAIOR.

Com isso:
    - buscar/inserir/remover descem por um único caminho (O(h));
    - o menor nome é o nó mais à esquerda; o maior, o mais à direita.
"""


class NoArvore:
    def __init__(self, pessoa):
        self.pessoa = pessoa
        self.esquerda = None
        self.direita = None

    @property
    def chave(self):
        return self.pessoa.nome


class ArvoreBinariaBusca:
    def __init__(self):
        self.raiz = None

    # ------------------------------------------------------------ inserção
    def inserir(self, pessoa):
        """Inserção iterativa. Retorna False se o nome já existir."""
        novo = NoArvore(pessoa)
        if self.raiz is None:
            self.raiz = novo
            return True
        atual = self.raiz
        while True:
            if pessoa.nome < atual.chave:
                if atual.esquerda is None:
                    atual.esquerda = novo
                    return True
                atual = atual.esquerda
            elif pessoa.nome > atual.chave:
                if atual.direita is None:
                    atual.direita = novo
                    return True
                atual = atual.direita
            else:
                return False    # nome repetido: não insere

    # --------------------------------------------------------------- busca
    def buscar(self, nome):
        """Busca iterativa. Retorna a Pessoa ou None."""
        atual = self.raiz
        while atual is not None:
            if nome == atual.chave:
                return atual.pessoa
            atual = atual.esquerda if nome < atual.chave else atual.direita
        return None

    # --------------------------------------------------------- mín. e máx.
    def minimo(self):
        """Primeira pessoa em ordem alfabética (nó mais à esquerda)."""
        if self.raiz is None:
            return None
        atual = self.raiz
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual.pessoa

    def maximo(self):
        """Última pessoa em ordem alfabética (nó mais à direita)."""
        if self.raiz is None:
            return None
        atual = self.raiz
        while atual.direita is not None:
            atual = atual.direita
        return atual.pessoa

    # ------------------------------------------------------------- remoção
    def remover(self, nome):
        """Remove o nó com a chave 'nome'. Retorna a Pessoa removida ou None."""
        self.raiz, removida = self._remover(self.raiz, nome)
        return removida

    def _remover(self, no, nome):
        # Retorna (nova raiz desta subárvore, pessoa removida)
        if no is None:
            return None, None
        if nome < no.chave:
            no.esquerda, removida = self._remover(no.esquerda, nome)
            return no, removida
        if nome > no.chave:
            no.direita, removida = self._remover(no.direita, nome)
            return no, removida

        # Achou o nó a remover
        removida = no.pessoa
        # Caso 1 e 2: nenhum filho ou apenas um filho
        if no.esquerda is None:
            return no.direita, removida
        if no.direita is None:
            return no.esquerda, removida
        # Caso 3: dois filhos -> substitui pelo SUCESSOR
        # (menor nó da subárvore direita)
        sucessor = no.direita
        while sucessor.esquerda is not None:
            sucessor = sucessor.esquerda
        no.pessoa = sucessor.pessoa
        no.direita, _ = self._remover(no.direita, sucessor.chave)
        return no, removida

    # -------------------------------------------------------------- outros
    def esta_vazia(self):
        return self.raiz is None

    def em_ordem(self):
        """Percurso em ordem (esquerda, raiz, direita) = ordem alfabética."""
        resultado = []

        def visitar(no):
            if no is not None:
                visitar(no.esquerda)
                resultado.append(no.pessoa)
                visitar(no.direita)

        visitar(self.raiz)
        return resultado


def gerar_arvore_da_lista(lista_encadeada):
    """
    Gera uma ABB a partir da lista encadeada simples (exigência do
    enunciado antes das operações do diretor). Percorre a lista do
    início ao fim e insere cada pessoa na árvore, usando o nome como chave.
    """
    arvore = ArvoreBinariaBusca()
    for pessoa in lista_encadeada:
        arvore.inserir(pessoa)
    return arvore
