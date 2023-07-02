import pandas as pd
import ast

def grafico_pie_p15(df_exportacao:pd.DataFrame):
    df_p15 = df_exportacao.sort_values(by='Total em US$', ascending=False).head(15)
    df_outros = df_exportacao.sort_values(by='Total em US$', ascending=True).head(
        df_exportacao.shape[0] - 15
    )

    df_p15_outros_paises = {
    'grupo': [],
    'total_dolares': []
    }

    df_p15_outros_paises['grupo'].append('P15')
    df_p15_outros_paises['total_dolares'].append(df_p15['Total em US$'].sum())
    df_p15_outros_paises['grupo'].append('Outros')
    df_p15_outros_paises['total_dolares'].append(df_outros['Total em US$'].sum())

    df_p15_outros_paises = pd.DataFrame(df_p15_outros_paises)
    return df_p15_outros_paises

def grafico_bar_p15_by_regiao(df_exportacao:pd.DataFrame):
    df_p15 = df_exportacao.sort_values(by='Total em US$', ascending=False).head(15)
    regioes = ["America","Europa","America","Europa","Asia","Europa","Europa","Europa","Asia","Africa","Europa","America","Europa",
           "Europa","Europa"]
    df_p15['regiao'] = regioes
    s_p15_regiao = df_p15.groupby('regiao')['Total em US$'].sum()
    return s_p15_regiao


def grafico_line_p15_by_regiao(df_exportacao:pd.DataFrame):
    """"
        Gera um dataframe para renderizar o gráfico para mostrar a tendencia
        de exportação em dólar por cada região
    """
    df_p15 = df_exportacao.sort_values(by='Total em US$', ascending=False).head(15)
    del df_p15['Total em US$']
    regioes = ["America","Europa","America","Europa","Asia","Europa","Europa","Europa","Asia","Africa","Europa","America","Europa",
           "Europa","Europa"]
    df_p15['regiao'] = regioes


    return df_p15.groupby('regiao').sum()

def grafico_bar_p15_by_socio(df_exportacao:pd.DataFrame):
    df_exportacao = df_exportacao.sort_values(by='Total em US$', ascending=False).head(15)
    df_exportacao['socio_economico'] = 'Desenvolvido'
    desenv = 'Desenvolvido'
    list_desenv = [2,3,5,6,7,8,9,11,12,13,14,15]
    subdesen = 'Subdesenvolvido'
    list_subdesen = [0,9]
    emerg = 'Emergente'
    list_emerg = [1,4]
    df_exportacao.iloc[list_subdesen, -1] = subdesen
    df_exportacao.iloc[list_emerg, -1] = emerg
    df_exportacao = df_exportacao.groupby('socio_economico').sum()

    return df_exportacao

def grafico_line_p15_by_socio(df_exportacao:pd.DataFrame):
    df_exportacao = df_exportacao.sort_values(by='Total em US$', ascending=False).head(15)
    df_exportacao['socio_economico'] = 'Desenvolvido'
    desenv = 'Desenvolvido'
    list_desenv = [2,3,5,6,7,8,9,11,12,13,14,15]
    subdesen = 'Subdesenvolvido'
    list_subdesen = [0,9]
    emerg = 'Emergente'
    list_emerg = [1,4]
    df_exportacao.iloc[list_subdesen, -1] = subdesen
    df_exportacao.iloc[list_emerg, -1] = emerg

    df_exportacao = df_exportacao.groupby('socio_economico').sum()

    return df_exportacao

def grafico_bar_p15_qtde_by_socio(df_exportacao:pd.DataFrame):
    df_exportacao = df_exportacao.sort_values(by='Total em US$', ascending=False).head(15)
    df_exportacao['socio_economico'] = 'Desenvolvido'
    desenv = 'Desenvolvido'
    list_desenv = [2,3,5,6,7,8,9,11,12,13,14,15]
    subdesen = 'Subdesenvolvido'
    list_subdesen = [0,9]
    emerg = 'Emergente'
    list_emerg = [1,4]
    df_exportacao.iloc[list_subdesen, -1] = subdesen
    df_exportacao.iloc[list_emerg, -1] = emerg

    df_exportacao = df_exportacao.groupby('socio_economico')['Total em US$'].count()
    df_exportacao.rename('Quantidade de paises', inplace=True)

    return df_exportacao

def df_gdp(df_exportacao:pd.DataFrame):
    # Lendo e filtrando
    df_gpd = pd.read_csv('../Dados/tech-challenge/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_5607117.csv', header=2)
    df_gpd_part_one = df_gpd.iloc[:,0:2]
    df_gpd_part_two = df_gpd.iloc[:,51:-2]

    df_gpd = pd.concat([df_gpd_part_one, df_gpd_part_two], axis=1)

    # Alocando os paises com o nome traduzidos
    lista_paises = ''

    with open('paises_traduzidos.txt', 'r', encoding='UTF-8') as paises:
        linha = paises.readline()
        lista_paises = linha

    lista_paises = ast.literal_eval(lista_paises)
    df_gpd.insert(1, 'pais',value=lista_paises)
    p15 = df_exportacao.head(15).index.to_list()

    # Russia/ Paises baixos / Alemanha
    # Comparando com o nosso df
    df_gpd['pais'] = df_gpd['pais'].str.strip()
    return df_gpd.query('pais in @p15 | pais=="Alemanha" | pais.str.startswith("R")')
    