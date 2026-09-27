# ED-ProjetoFinal — Sistema de Lista de Espera Escolar

Projeto Final da disciplina **Estrutura de Dados** — FGV, Análise e Desenvolvimento de Sistemas.
Autor: **Vinicius Costa**

Sistema de cadastro da lista de espera de uma escola no **Guarujá (SP)**, usado em sequência por três perfis de funcionários. Cada perfil utiliza uma estrutura de dados diferente, escolhida de acordo com o tipo de operação que realiza.

| Perfil | Estrutura de dados | Operações |
|---|---|---|
| Secretário(a) | Lista encadeada simples | Cadastrar pessoa (com cidade sorteada do CSV), consultar por nome, ver quantidade |
| Diretor(a) | Árvore binária de busca (chave = nome), gerada a partir da lista | Editar nome/idade/telefone, descadastrar, primeira e última pessoa em ordem alfabética |
| Assistente | Grafo ponderado não-direcionado (a partir de `cidades_vizinhas.csv`) + Dijkstra | Menor caminho até a cidade da pessoa, menor caminho passando por Indaiatuba, cidade mais próxima com moradores |

## Como executar

Requisitos: **Python 3.8+** (não usa bibliotecas externas).

```bash
python3 main.py
```

O arquivo `cidades_vizinhas.csv` deve estar na mesma pasta dos arquivos `.py`.

## Organização do código

```
├── main.py                      # Interface: menus e leitura do teclado
├── atribuicoes_secretario.py    # Ponte main ↔ lista encadeada
├── atribuicoes_diretor.py       # Ponte main ↔ árvore binária de busca
├── atribuicoes_assistente.py    # Ponte main ↔ grafo
├── pessoa.py                    # Classe Pessoa
├── lista_encadeada.py           # Lista encadeada simples
├── arvore_binaria.py            # Árvore binária de busca
├── grafo.py                     # Grafo, leitura do CSV e Dijkstra
└── cidades_vizinhas.csv         # cidade1, cidade2, distância
```

Conforme o enunciado, o `main.py` **não acessa diretamente** nenhuma estrutura de dados: ele só chama as funções dos arquivos `atribuicoes_*.py`.

## Decisões de implementação

- **Lista encadeada:** mantém ponteiros para o início e o fim, o que torna a inserção O(1), e um contador de tamanho.
- **Árvore binária de busca:** é gerada a partir da lista quando o(a) diretor(a) assume o sistema. Como o nome é a chave, alterar o nome de uma pessoa **remove o nó e o reinsere** na posição correta. A remoção trata os três casos: nó sem filhos, com um filho e com dois filhos (usando o sucessor).
- **Grafo:** usa lista de adjacência. Cada linha do CSV gera arestas nos dois sentidos, porque o grafo é não-direcionado.
- **Dijkstra:** usa fila de prioridade (`heapq`). O caminho via Indaiatuba é a junção de dois menores caminhos (Guarujá → Indaiatuba e Indaiatuba → destino). A cidade mais próxima com moradores é encontrada com uma única execução do Dijkstra a partir do Guarujá.

## Validações

- Menus reexibidos até que uma opção válida seja informada. Letras e campos vazios também são tratados.
- Mensagem para pessoa não cadastrada em todas as buscas por nome.
- Idade aceita apenas números inteiros, e nenhum campo pode ficar vazio.
- Nomes únicos: impede cadastrar ou renomear para um nome que já existe.
- Confirmação de descadastro aceita apenas S ou N.
- Mensagens específicas para lista de espera vazia.

## Exemplo de execução (assistente)

```
Digite o nome da pessoa cuja cidade te interessa: Mariana
Nome: Mariana | Idade: 32 | Telefone: 7891-1121 | Cidade: Vargem Grande Paulista
Menor caminho = ['Guarujá', 'Santos', 'São Bernardo do Campo', 'São Paulo', 'Vargem Grande Paulista'] com custo 127
```
