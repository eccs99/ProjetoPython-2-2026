# Projeto: Análise de Dados com Python — Catálogo da Netflix

**Disciplina:** Linguagem de Programação em Python (2026.2)  
**Professor:** Ruben Prado  
**Instituição:** Faculdade Senac-DF de Tecnologia e Inovação

---

## Objetivo do Projeto

Este projeto consolida os conhecimentos do semestre. A equipe desenvolveu um sistema de análise com menu interativo no terminal para explorar o catálogo de filmes e séries da Netflix.

O sistema lê uma base de dados do Kaggle, usa Pandas para tratar e analisar os dados, organiza as operações em uma classe Python e gera gráficos com Matplotlib e Seaborn.

---

## Estrutura do Repositório

```text
projeto_netflix/
├── data/
│   └── netflix_titles_nov_2019.csv
├── src/
│   ├── __init__.py
│   └── analisador.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Requisitos Técnicos

| Requisito | Como foi atendido |
|---|---|
| **Menu interativo (`main.py`)** | O menu roda em um laço `while True`. Se a opção digitada não puder ser convertida em um número inteiro, o `try/except ValueError` exibe a mensagem “Digite apenas números.” e volta ao menu. Se o CSV não for encontrado, o programa informa o caminho esperado e encerra. |
| **Análise de dados (`src/analisador.py`)** | O CSV é lido com `pd.read_csv()`. O método privado `__limpar_dados()` prepara os campos de país, gênero, classificação indicativa, ano de adição e duração. As análises usam `groupby()`, `value_counts()` e filtros conforme a opção escolhida. |
| **Orientação a objetos** | A classe `AnalisadorNetflix` guarda o catálogo e os filmes nos atributos privados `self.__dados` e `self.__filmes`. O `main.py` carrega o catálogo, exibe o menu e chama o método correspondente à opção escolhida. |
| **Visualização** | O sistema gera cinco gráficos com títulos e eixos identificados. São um gráfico de linha, dois de barras, um histograma e um gráfico de dispersão. |

---

## Instalação e Execução Local

Coloque o arquivo `netflix_titles_nov_2019.csv` na pasta `data/`. Abra o terminal na raiz do projeto e execute:

```bash
pip install -r requirements.txt
python main.py
```

No Windows, caso o comando `python` não seja reconhecido, use `py -m pip install -r requirements.txt` e `py main.py`.

### Opções do Menu

```text
======= ANÁLISE NETFLIX =======
1 - Resumo geral
2 - Quantidade de filmes e séries
3 - Top 10 gêneros principais
4 - Buscar título
5 - Títulos por país principal
6 - Títulos adicionados por ano
7 - 10 países principais com mais títulos
8 - Títulos por classificação indicativa
9 - Histograma da duração dos filmes
10 - Ano de lançamento e duração dos filmes
0 - Sair
```

- As opções de 1 a 5 exibem resultados no terminal. Na opção 5, digite o nome do país em inglês, como `Brazil`.
- As opções de 6 a 10 abrem os gráficos. Feche a janela do gráfico para voltar ao menu.
- A opção 0 encerra o programa.
- Quando um título tem vários países ou gêneros, o programa usa o primeiro item de cada lista nas análises de país ou gênero principal.

---

## Como Entregar pelo GitHub

1. Faça um fork ou clone do repositório da atividade.
2. Crie a branch da equipe com `git checkout -b dev-nome-da-equipe`.
3. Divida o trabalho entre os integrantes e registre as alterações em commits.
4. Envie a branch com `git push origin dev-nome-da-equipe`.
5. Abra um Pull Request da branch da equipe para a `main`.

---

## Formulário Oficial de Entrega

### Integrantes da Equipe

- Eric Santos — 2026.15.292
- Mateus Monteiro — 2026.15.208
- Diogo Gouvêa — 2026.15.1431
- Fábio Silveira — 2026.15.3
- Yuri Bering — 2026.15.128

### Sobre o Dataset Escolhido

Escolhemos esse dataset para analisar o crescimento do catálogo da Netflix, abordando a origem das obras, os gêneros e classificações indicativas mais frequentes.
A base reúne 5.837 títulos, sendo 3.939 filmes e 1.898 séries, do catálogo de novembro de 2019.


[Netflix Movies and TV Shows (versão 2) — Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows/versions/2)

### Arquitetura e Limpeza dos Dados

No arquivo `src/analisador.py`, a classe `AnalisadorNetflix` lê o CSV, guarda o catálogo em `self.__dados` e executa `__limpar_dados()`. A classe calcula estatísticas, busca títulos pelo nome ou pelo país principal e gera os gráficos. Usamos `groupby()` com `size()` para contar os títulos adicionados a cada ano e `value_counts()` para contar os títulos por gênero principal.

A base possui valores ausentes em `director` (1.901), `date_added` (642), `cast` (556), `country` (427) e `rating` (10). Aplicar `dropna()` em toda a base deixaria 3.447 dos 5.837 títulos. Para preservar os registros, usamos `fillna("Não informado")` nas colunas `country`, `rating` e `listed_in`.

Títulos sem país continuam na contagem geral e ficam fora do ranking de países. A análise anual considera os títulos com ano de adição extraído de `date_added`. As análises de duração consideram os filmes com duração válida em minutos.

### Gráficos Desenvolvidos

1. **Títulos adicionados por ano:** gráfico de linha que mostra quantos títulos entraram no catálogo a cada ano.
2. **Países com mais títulos:** gráfico de barras horizontais com os 10 países que mais aparecem como país principal.
3. **Classificação indicativa:** gráfico de barras verticais com a quantidade de títulos por classificação.
4. **Duração dos filmes:** histograma que mostra quantos filmes estão em cada uma das 25 faixas de duração, medidas em minutos.
5. **Ano de lançamento e duração:** gráfico de dispersão que compara o ano de lançamento com a duração dos filmes em minutos.

---

## Tecnologias

- **Python 3** para o menu e a estrutura do programa.
- **Pandas** para leitura, limpeza e análise dos dados.
- **Matplotlib** e **Seaborn** para os gráficos.
