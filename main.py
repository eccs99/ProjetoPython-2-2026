from src.analisador import AnalisadorNetflix


def mostrar_menu():
    """Exibe as opções de análise do catálogo."""
    print()
    print("======= ANÁLISE NETFLIX =======")
    print("1 - Resumo geral")
    print("2 - Quantidade de filmes e séries")
    print("3 - Top 10 gêneros principais")
    print("4 - Buscar título")
    print("5 - Títulos por país principal")
    print("6 - Títulos adicionados por ano")
    print("7 - 10 países principais com mais títulos")
    print("8 - Títulos por classificação indicativa")
    print("9 - Histograma da duração dos filmes")
    print("10 - Ano de lançamento e duração dos filmes")
    print("0 - Sair")


def iniciar_sistema():
    """Carrega o catálogo e executa o menu interativo."""
    caminho_csv = "data/netflix_titles_nov_2019.csv"

    try:
        analisador = AnalisadorNetflix(caminho_csv)
    except FileNotFoundError:
        print(f"Arquivo CSV não encontrado: {caminho_csv}")
        return

    while True:
        mostrar_menu()
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite apenas números.")
            continue

        print()
        if opcao == 1:
            analisador.resumo_geral()
        elif opcao == 2:
            analisador.contagem_por_tipo()
        elif opcao == 3:
            analisador.top_generos()
        elif opcao == 4:
            titulo = input("Nome do título: ")
            analisador.buscar_titulo(titulo)
        elif opcao == 5:
            pais = input("País em inglês (ex: Brazil): ")
            analisador.titulos_do_pais(pais)
        elif opcao == 6:
            analisador.grafico_linha_titulos_por_ano()
        elif opcao == 7:
            analisador.grafico_barras_top_paises()
        elif opcao == 8:
            analisador.grafico_barras_classificacao()
        elif opcao == 9:
            analisador.grafico_histograma_duracao()
        elif opcao == 10:
            analisador.grafico_dispersao_ano_duracao()
        elif opcao == 0:
            print("Encerrando o programa!")
            break
        else:
            print("Digite um número do menu.")


if __name__ == "__main__":
    iniciar_sistema()