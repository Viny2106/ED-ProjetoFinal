"""
main.py
Interface com o usuário: menus e leitura do teclado.

Regra do enunciado: este arquivo NÃO acessa Lista Encadeada, Árvore ou
Grafo. Ele só conversa com os módulos atribuicoes_*.py.
"""

import atribuicoes_secretario as secretario
import atribuicoes_diretor as diretor
import atribuicoes_assistente as assistente

MSG_NAO_CADASTRADA = "Pessoa não cadastrada. Tem certeza que o nome está certo?"
MSG_NAO_CADASTRADA_OU_VAZIA = ("Pessoa não cadastrada ou lista de espera vazia. "
                               "Tem certeza que o nome da pessoa está certo?")


# ====================================================== funções auxiliares
def boas_vindas(perfil):
    print(f"\n-------------- Olá, {perfil}! --------------")


def ler_opcao(menu, minimo, maximo):
    """Mostra o menu até o usuário digitar uma opção válida (validação)."""
    while True:
        print("\n" + menu)
        entrada = input("Digite sua opção: ").strip()
        if entrada.isdigit() and minimo <= int(entrada) <= maximo:
            return int(entrada)
        print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")


def ler_texto(mensagem):
    """Não aceita texto vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Valor inválido. O campo não pode ficar vazio.")


def ler_idade(mensagem):
    """Só aceita número inteiro entre 0 e 130."""
    while True:
        entrada = input(mensagem).strip()
        if entrada.isdigit() and 0 <= int(entrada) <= 130:
            return int(entrada)
        print("Idade inválida. Digite um número inteiro (ex.: 23).")


# ============================================================ SECRETÁRIO(A)
MENU_SECRETARIO = """Você deseja:
(1) Cadastrar nova pessoa na lista de espera.
(2) Consultar pessoa cadastrada.
(3) Ver quantidade de pessoas cadastradas.
(4) Finalizar execução."""


def executar_secretario():
    boas_vindas("Secretário(a)")
    while True:
        opcao = ler_opcao(MENU_SECRETARIO, 1, 4)

        if opcao == 1:
            nome = ler_texto("Digite o nome da pessoa: ")
            if secretario.nome_ja_cadastrado(nome):
                print("Já existe uma pessoa com esse nome na lista de espera.")
                continue
            idade = ler_idade("Digite a idade: ")
            telefone = ler_texto("Digite o telefone: ")
            print(secretario.cadastrar_pessoa(nome, idade, telefone))

        elif opcao == 2:
            nome = ler_texto("Digite o nome da pessoa: ")
            dados = secretario.consultar_pessoa(nome)
            print(dados if dados else MSG_NAO_CADASTRADA)

        elif opcao == 3:
            qtd = secretario.quantidade_pessoas()
            if qtd == 1:
                print("É 1 pessoa na lista de espera.")
            else:
                print(f"São {qtd} pessoas na lista de espera.")

        else:  # opção 4
            print("Fim das atividades sob responsabilidade do(a) Secretário(a).\n")
            return


# =============================================================== DIRETOR(A)
MENU_DIRETOR = """Você deseja:
(1) Alterar nome, idade ou telefone de pessoa cadastrada.
(2) Descadastrar pessoa.
(3) Obter informações da primeira pessoa em ordem alfabética de nome.
(4) Obter informações da última pessoa em ordem alfabética de nome.
(5) Confirmar validade da lista de espera e finalizar execução."""


def editar_pessoa():
    nome = ler_texto("Digite o nome da pessoa que você quer editar: ")
    dados = diretor.consultar_pessoa(nome)
    if dados is None:
        print(MSG_NAO_CADASTRADA)
        return
    print(dados)

    while True:
        campo = input("O que você quer editar? Digite 1 para nome, "
                      "2 para idade ou 3 para telefone: ").strip()
        if campo in ("1", "2", "3"):
            break
        print("Opção inválida.")

    if campo == "1":
        novo_nome = ler_texto("Digite o novo nome: ")
        if novo_nome != nome and diretor.nome_ja_cadastrado(novo_nome):
            print("Já existe uma pessoa com esse nome. Alteração cancelada.")
            return
        diretor.alterar_nome(nome, novo_nome)
    elif campo == "2":
        diretor.alterar_idade(nome, ler_idade("Digite a nova idade: "))
    else:
        diretor.alterar_telefone(nome, ler_texto("Digite o novo telefone: "))
    print("Dados atualizados com sucesso.")


def descadastrar_pessoa():
    nome = ler_texto("Digite o nome da pessoa que você quer descadastrar: ")
    dados = diretor.consultar_pessoa(nome)
    if dados is None:
        print(MSG_NAO_CADASTRADA_OU_VAZIA)
        return
    print(dados)

    while True:
        resposta = input(f"Tem certeza que deseja descadastrar {nome}? "
                         "Digite S ou N: ").strip().upper()
        if resposta in ("S", "N"):
            break
        print("Resposta inválida. Digite S ou N.")

    if resposta == "S":
        diretor.descadastrar_pessoa(nome)
        print(f"{nome} descadastrado com sucesso.")
    else:
        print("Operação cancelada.")


def executar_diretor():
    boas_vindas("Diretor(a)")
    diretor.preparar_arvore()     # gera a ABB a partir da lista encadeada
    while True:
        opcao = ler_opcao(MENU_DIRETOR, 1, 5)
        if opcao == 1:
            editar_pessoa()
        elif opcao == 2:
            descadastrar_pessoa()
        elif opcao in (3, 4):
            dados = (diretor.primeira_pessoa_alfabetica() if opcao == 3
                     else diretor.ultima_pessoa_alfabetica())
            print(dados if dados else "A lista de espera está vazia.")
        else:  # opção 5
            print("Fim das atividades sob responsabilidade do(a) Diretor(a).\n")
            return


# =============================================================== ASSISTENTE
MENU_ASSISTENTE = """Você deseja:
(1) Ver a menor distância entre a cidade da escola e a cidade de uma pessoa.
(2) Ver a menor distância da cidade da escola até a cidade da pessoa passando por uma cidade específica.
(3) Ver dados da(s) pessoa(s) que mora(m) na cidade mais perto da cidade da escola (incluindo distância).
(4) Finalizar execução."""


def executar_assistente():
    boas_vindas("Assistente")
    while True:
        opcao = ler_opcao(MENU_ASSISTENTE, 1, 4)

        if opcao in (1, 2):
            nome = ler_texto("Digite o nome da pessoa cuja cidade te interessa: ")
            if opcao == 1:
                resultado = assistente.menor_caminho_ate_pessoa(nome)
            else:
                resultado = assistente.menor_caminho_via_intermediaria(nome)
            if resultado is None:
                print(MSG_NAO_CADASTRADA_OU_VAZIA)
            else:
                dados_pessoa, texto_caminho = resultado
                print(dados_pessoa)
                print(texto_caminho)

        elif opcao == 3:
            resultado = assistente.moradores_cidade_mais_proxima()
            if resultado is None:
                print("A lista de espera está vazia.")
            else:
                cidade, distancia, moradores = resultado
                print("A cidade mais próxima à cidade da escola que tem moradores "
                      f"na lista de espera (ver abaixo) é {cidade}. "
                      f"Distância = {distancia}")
                for morador in moradores:
                    print(morador)

        else:  # opção 4
            print("Fim da execução do sistema.")
            return


# ==================================================================== início
if __name__ == "__main__":
    executar_secretario()
    executar_diretor()
    executar_assistente()
