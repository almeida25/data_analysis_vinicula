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
    df_gpd = pd.read_csv('datasets/tech-challenge/content/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_5607117.csv', header=2)
    df_gpd_part_one = df_gpd.iloc[:,0:2]
    df_gpd_part_two = df_gpd.iloc[:,51:-2]

    df_gpd = pd.concat([df_gpd_part_one, df_gpd_part_two], axis=1)

    # Alocando os paises com o nome traduzidos
    lista_paises = ''

    with open('datasets/tech-challenge/content/paises_traduzidos.txt', 'r', encoding='UTF-8') as paises:
        linha = paises.readline()
        lista_paises = linha

    lista_paises = ast.literal_eval(lista_paises)
    df_gpd.insert(1, 'pais',value=lista_paises)
    p15 = df_exportacao.head(15).index.to_list()

    # Russia/ Paises baixos / Alemanha
    # Comparando com o nosso df
    df_gpd['pais'] = df_gpd['pais'].str.strip()
    return df_gpd.query('pais in @p15 | pais=="Alemanha" | pais.str.startswith("R")')
    
def grafico_bar_mercosul(df_exportacao:pd.DataFrame):
    paises_mercosul = ['Bolívia','Uruguai','Argentina','Chile','Colômbia','Peru','Equador','Guiana','Suriname']
    return df_exportacao.loc[paises_mercosul]


def grafico_bar_continentes(df_exportacao:pd.DataFrame):
    df_exp_maiores_lucros_regiao = df_exportacao.copy()
    df_exp_maiores_lucros_regiao.insert(column='id',loc=0,value=range(df_exportacao.shape[0]))

    # Filtrando valores
    america = [0,2,11,24,26,27,29,30,32,35,36,40,41,44,45,49,50,52,54,63,69,71,74,78,79,82,84,87,88,92,97,103,106,108,110]
    asia = [4,8,20,25,37,42,48,57,60,62,65,70,76,90,91,93,98,101,102,104,112]
    europa = [1,3,5,6,7,10,12,13,14,16,17,18,21,22,23,28,33,34,38,56,58,61,64,72,73,75,77,81,83,85,94,95,100]
    africa = [9,15,31,39,46,51,53,55,58,67,68,80, 86, 89,96,109,111]
    oceania = [19,43,47,66,107,113]

    # Resetando index
    df_exp_maiores_lucros_regiao.index = df_exp_maiores_lucros_regiao['id']

    # Alocando continentes
    df_exp_maiores_lucros_regiao.loc[oceania, 'continente'] = 'Oceania'
    df_exp_maiores_lucros_regiao.loc[africa, 'continente'] = 'Africa'
    df_exp_maiores_lucros_regiao.loc[asia, 'continente'] = 'Asia'
    df_exp_maiores_lucros_regiao.loc[america, 'continente'] = 'America'
    df_exp_maiores_lucros_regiao.loc[europa, 'continente'] = 'Europa'

    df_exp_maiores_lucros_regiao.index = df_exportacao.index

    return df_exp_maiores_lucros_regiao


## Para ajudar a gerar os outros gráficos 
# Gráfico do Merco Sul -
# df para gerar o gráfico
"""

"""

# Gráfico dos continentes-
# df para gerar o gráfico dos continentes

"""
# GERA UMA COPIA E ADICIONA UM ID
df_exp_maiores_lucros_regiao = df_exp_vinho_maiores_lucros.copy()
df_exp_maiores_lucros_regiao.insert(column='id',loc=0,value=range(df_exp_vinho_maiores_lucros.shape[0]))


# MONTA OS FILTROS
#https://mundoeducacao.uol.com.br/geografia/paises.htm
america = [0,2,11,24,26,27,29,30,32,35,36,40,41,44,45,49,50,52,54,63,69,71,74,78,79,82,84,87,88,92,97,103,106,108,110]
america_s = [str(x) for x in america]

asia = [4,8,20,25,37,42,48,57,60,62,65,70,76,90,91,93,98,101,102,104,112]
asia_s = [str(x) for x in asia]

europa = [1,3,5,6,7,10,12,13,14,16,17,18,21,22,23,28,33,34,38,56,58,61,64,72,73,75,77,81,83,85,94,95,100]
europa_s = [str(x) for x in europa]

africa = [9,15,31,39,46,51,53,55,58,67,68,80, 86, 89,96,109,111]
africa_s = [str(x) for x in africa]

oceania = [19,43,47,66,107,113]
oceania_s = [str(x) for x in oceania]

ALTERA O ID COMO INDEX (DEPOIS VOLTA A OPERAÇÃO COM O OUTRO DF)
df_exp_maiores_lucros_regiao.index = df_exp_maiores_lucros_regiao['id']

FUNÇÃO PARA SER CHAMADA NO APPLY
ADICIONAR PARA OS OUTROS CONTINENTES
ESTÁ DANDO ERRO ->>>>
def set_regiao(df):
    if df['id'] in oceania_s:
        print('True')
        df['continente'] = 'Oceania'

df_exp_maiores_lucros_regiao.apply(set_regiao, axis=0)
"""
