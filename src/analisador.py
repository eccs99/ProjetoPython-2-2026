import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class AnalisadorNetflix:
    """Analisa um catálogo da Netflix carregado de um arquivo CSV."""

    def __init__(self, caminho_csv):
        self.__dados = pd.read_csv(caminho_csv)
        self.__limpar_dados()
        self.__filmes = self.__dados[self.__dados["type"] == "Movie"]

    def __limpar_dados(self):
        """Prepara as colunas usadas nas análises do catálogo."""
        self.__dados["country"] = self.__dados["country"].fillna("Não informado")
        self.__dados["rating"] = self.__dados["rating"].fillna("Não informado")
        self.__dados["listed_in"] = self.__dados["listed_in"].fillna("Não informado")

        # O primeiro país e o primeiro gênero são usados nas contagens.
        paises = []
        for pais in self.__dados["country"]:
            paises.append(pais.split(",")[0].strip())
        self.__dados["pais_principal"] = paises

        generos = []
        for genero in self.__dados["listed_in"]:
            generos.append(genero.split(",")[0].strip())
        self.__dados["genero_principal"] = generos

        # O ano aparece nos quatro últimos caracteres da data.
        anos = []
        for data in self.__dados["date_added"].fillna(""):
            anos.append(str(data).strip()[-4:])
        self.__dados["ano_adicao"] = pd.to_numeric(anos, errors="coerce")

        # Somente durações em minutos entram nas análises de filmes.
        minutos = []
        for duracao in self.__dados["duration"].fillna(""):
            if duracao.endswith(" min"):
                minutos.append(duracao[:-4])
            else:
                minutos.append(None)
        self.__dados["duracao_minutos"] = pd.to_numeric(minutos, errors="coerce")

    def resumo_geral(self):
        series = self.__dados[self.__dados["type"] == "TV Show"]
        com_pais = self.__dados[self.__dados["pais_principal"] != "Não informado"]

        print("Total de títulos:", len(self.__dados))
        print("Quantidade de filmes:", len(self.__filmes))
        print("Quantidade de séries:", len(series))
        print("Países diferentes (país principal):", len(com_pais["pais_principal"].unique()))
        print("Gêneros diferentes (gênero principal):", len(self.__dados["genero_principal"].unique()))
        print("Ano de lançamento mais antigo:", self.__dados["release_year"].min())
        print("Ano de lançamento mais recente:", self.__dados["release_year"].max())
        print("Duração média dos filmes (min):", round(self.__filmes["duracao_minutos"].mean(), 1))
        print("Títulos com data de adição:", self.__dados["ano_adicao"].count())

    def contagem_por_tipo(self):
        contagem = self.__dados.groupby("type").size()
        print("Filmes:", contagem.get("Movie", 0))
        print("Séries:", contagem.get("TV Show", 0))

    def top_generos(self):
        contagem = self.__dados["genero_principal"].value_counts().head(10)
        for genero in contagem.index:
            print(f"{genero}: {contagem[genero]}")

    def buscar_titulo(self, titulo):
        """Mostra até 20 títulos que contêm o texto digitado."""
        titulo = titulo.strip().lower()
        if not titulo:
            print("Digite um título para buscar.")
            return

        encontrados = 0
        for i in self.__dados.index:
            nome = self.__dados.loc[i, "title"]
            if pd.notna(nome) and titulo in nome.lower():
                tipo = self.__dados.loc[i, "type"]
                ano = self.__dados.loc[i, "release_year"]
                pais = self.__dados.loc[i, "country"]
                classificacao = self.__dados.loc[i, "rating"]
                generos = self.__dados.loc[i, "listed_in"]
                print(f"{nome} | {tipo} | {ano} | {pais} | {classificacao} | {generos}")

                encontrados += 1
                if encontrados == 20:
                    break

        if encontrados == 0:
            print("Título não encontrado.")

    def titulos_do_pais(self, pais):
        """Mostra até 15 títulos recentes do país principal informado."""
        pais = pais.strip().lower()
        encontrados = []
        for i in self.__dados.index:
            if self.__dados.loc[i, "pais_principal"].lower() == pais:
                encontrados.append(i)

        titulos = self.__dados.loc[encontrados].sort_values(
            "release_year", ascending=False
        )
        print(f"Total encontrado: {len(titulos)}")

        for i in titulos.head(15).index:
            nome = titulos.loc[i, "title"]
            tipo = titulos.loc[i, "type"]
            ano = titulos.loc[i, "release_year"]
            pais_titulo = titulos.loc[i, "country"]
            print(f"{nome} | {tipo} | {ano} | {pais_titulo}")

    def grafico_linha_titulos_por_ano(self):
        contagem = self.__dados.groupby("ano_adicao").size()

        plt.figure(figsize=(10, 5))
        plt.plot(contagem.index, contagem.values, marker="o")
        plt.title("Títulos adicionados à Netflix por ano (2019 parcial, até novembro)")
        plt.xlabel("Ano")
        plt.ylabel("Quantidade de títulos")
        plt.show()

    def grafico_barras_top_paises(self):
        com_pais = self.__dados[self.__dados["pais_principal"] != "Não informado"]

        # A ordenação coloca a maior barra no topo.
        dez_paises = com_pais["pais_principal"].value_counts().head(10).sort_values()

        plt.figure(figsize=(10, 5))
        plt.barh(dez_paises.index, dez_paises.values)
        plt.title("10 países principais com mais títulos")
        plt.xlabel("Quantidade de títulos")
        plt.ylabel("País")
        plt.tight_layout()
        plt.show()

    def grafico_barras_classificacao(self):
        contagem = self.__dados["rating"].value_counts()

        plt.figure(figsize=(10, 5))
        plt.bar(contagem.index, contagem.values)
        plt.title("Títulos por classificação indicativa")
        plt.xlabel("Classificação")
        plt.ylabel("Quantidade de títulos")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def grafico_histograma_duracao(self):
        plt.figure(figsize=(10, 5))
        plt.hist(self.__filmes["duracao_minutos"].dropna(), bins=25)
        plt.title("Duração dos filmes")
        plt.xlabel("Duração em minutos")
        plt.ylabel("Quantidade de filmes")
        plt.show()

    def grafico_dispersao_ano_duracao(self):
        plt.figure(figsize=(10, 5))
        sns.scatterplot(
            data=self.__filmes, x="release_year", y="duracao_minutos", alpha=0.4
        )
        plt.title("Ano de lançamento x duração dos filmes")
        plt.xlabel("Ano de lançamento")
        plt.ylabel("Duração em minutos")
        plt.show()
