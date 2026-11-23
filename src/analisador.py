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

        # valor em texto/remove espaços/pega ultimos 4 para numeros
        anos = []
        for data in self.__dados["date_added"].fillna(""):
            anos.append(str(data).strip()[-4:])
        self.__dados["ano_adicao"] = pd.to_numeric(anos, errors="coerce")

        # filme = minutos "90 min" / serie = temporadas "1" ou "2" [-4:] (pega) e [:-4] (retira)
        # else none para separa duração e temporada
        minutos = []
        for duracao in self.__dados["duration"].fillna(""):
            if duracao.endswith(" min"):
                minutos.append(duracao[:-4])
            else:
                minutos.append(None)
        self.__dados["duracao_minutos"] = pd.to_numeric(minutos, errors="coerce")

        #Type = serie e com_pais = contagem != diferente de
    def resumo_geral(self):
        series = self.__dados[self.__dados["type"] == "TV Show"]
        com_pais = self.__dados[self.__dados["pais_principal"] != "Não informado"]

      #unique = cada pais uma unica vez  len = quantos sobraram
      #maior ano e menor ano
      #mean  media e round arredonda
        print("Total de títulos:", len(self.__dados))
        print("Quantidade de filmes:", len(self.__filmes))
        print("Quantidade de séries:", len(series))
        print("Países diferentes (país principal):", len(com_pais["pais_principal"].unique()))
        print("Gêneros diferentes (gênero principal):", len(self.__dados["genero_principal"].unique()))
        print("Ano de lançamento mais antigo:", self.__dados["release_year"].min())
        print("Ano de lançamento mais recente:", self.__dados["release_year"].max())
        print("Duração média dos filmes (min):", round(self.__filmes["duracao_minutos"].mean(), 1))
        print("Títulos com data de adição:", self.__dados["ano_adicao"].count())

      #size conta as linhas de cada grrupo
    def contagem_por_tipo(self):
        contagem = self.__dados.groupby("type").size()
        print("Filmes:", contagem.get("Movie", 0))
        print("Séries:", contagem.get("TV Show", 0))

     #seleciona/organiza + e -/ pega os 10 primeiros/ contagem guarda junto com qtd
    def top_generos(self):
        contagem = self.__dados["genero_principal"].value_counts().head(10)
        for genero in contagem.index:
            print(f"{genero}: {contagem[genero]}")

    #remove espaços/transforma em minusculo/ vazio
    def buscar_titulo(self, titulo):
        """Mostra até 20 títulos que contêm o texto digitado."""
        titulo = titulo.strip().lower()
        if not titulo:
            print("Digite um título para buscar.")
            return
   
    #uma linha por vez/ i=linha atual/pandas transforma em minúsculo e segue
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


     #rremover espaços/transforma em minusculo/ vazio/loc = localiza e retorna o valor 
    def titulos_do_pais(self, pais):
        pais = pais.strip().lower()

        #linhas que correspondem ao pais.le a linha, compara e guarda
        encontrados = []
        for i in self.__dados.index:
            if self.__dados.loc[i, "pais_principal"].lower() == pais:
                encontrados.append(i)

        #recupera/orrganiza/ano. len conta todos os titulos e mostra o total
        titulos = self.__dados.loc[encontrados].sort_values(
            "release_year", ascending=False
        )
        print(f"Total encontrado: {len(titulos)}")

       #15 recentes, se tiver menos de 15 mostra todos
        for i in titulos.head(15).index:
            nome = titulos.loc[i, "title"]
            tipo = titulos.loc[i, "type"]
            ano = titulos.loc[i, "release_year"]
            pais_titulo = titulos.loc[i, "country"]
            print(f"{nome} | {tipo} | {ano} | {pais_titulo}")



#groupby reune/conta quantos titulos
    def grafico_linha_titulos_por_ano(self):
        contagem = self.__dados.groupby("ano_adicao").size()

        plt.figure(figsize=(10, 5))
        plt.plot(contagem.index, contagem.values, marker="o")
        plt.title("Títulos adicionados à Netflix por ano (2019 parcial, até novembro)")
        plt.xlabel("Ano")
        plt.ylabel("Quantidade de títulos")
        plt.show()

#top 10 paises com mais titulosq/remove os que nao tem pais/conta e pega os 10 primeiros
    def grafico_barras_top_paises(self):
        com_pais = self.__dados[self.__dados["pais_principal"] != "Não informado"]

        
        dez_paises = com_pais["pais_principal"].value_counts().head(10).sort_values()

        plt.figure(figsize=(10, 5))
        plt.barh(dez_paises.index, dez_paises.values)
        plt.title("10 países principais com mais títulos")
        plt.xlabel("Quantidade de títulos")
        plt.ylabel("País")
        plt.tight_layout()
        plt.show()

    #qual rating mais frequente/conta e organiza/mostra em grafico de barras
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

    #seleciona apenas os filmes/pega coluna de duracao e remove os nulos/mostra em histograma
    def grafico_histograma_duracao(self):
        plt.figure(figsize=(10, 5))
        plt.hist(self.__filmes["duracao_minutos"].dropna(), bins=25)
        plt.title("Duração dos filmes")
        plt.xlabel("Duração em minutos")
        plt.ylabel("Quantidade de filmes")
        plt.show()

    #grafico de dispersão/seleciona apenas os filmes/ano de lançamento x duração dos filmes
    def grafico_dispersao_ano_duracao(self):
        plt.figure(figsize=(10, 5))
        sns.scatterplot(
            data=self.__filmes, x="release_year", y="duracao_minutos", alpha=0.4
        )
        plt.title("Ano de lançamento x duração dos filmes")
        plt.xlabel("Ano de lançamento")
        plt.ylabel("Duração em minutos")
        plt.show()
