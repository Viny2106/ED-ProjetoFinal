"""
pessoa.py
Representa uma pessoa da lista de espera.

O MESMO objeto Pessoa é referenciado pela lista encadeada (secretário)
e pela árvore binária de busca (diretor). Assim, quando o diretor altera
idade ou telefone na árvore, a alteração vale para todo o sistema.
"""


class Pessoa:
    def __init__(self, nome, idade, telefone, cidade):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.cidade = cidade

    def __str__(self):
        return (f"Nome: {self.nome} | Idade: {self.idade} | "
                f"Telefone: {self.telefone} | Cidade: {self.cidade}")
