import json
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import plotly.graph_objs as go
from st_aggrid import AgGrid, GridOptionsBuilder
import scripts.analise as analise

PRIMARY_COLOR = "#572b52"

def main():
    
    st.set_page_config(page_title="Vitivinicultura Brasileira")
    st.header("Vitivinicultura Brasileira")
    st.write('')
    st.subheader("Introdução")
    st.write("A VitiBrasil é uma vinícola de renome internacional, dedicada à produção de vinhos excepcionais, e tem o prazer de compartilhar seu sucesso nas exportações nos últimos anos. Com base em sua expertise, qualidade incomparável e compromisso com a excelência, a VitiBrasil se estabeleceu como uma das principais marcas de vinhos do Brasil. Neste texto, destacaremos o crescimento impressionante das exportações da VitiBrasil e os motivos pelos quais investir nessa vinícola promissora é uma oportunidade única.")
    st.write("Nos últimos anos, a VitiBrasil tem ganhado destaque no cenário internacional como uma produtora de vinhos de alta qualidade e sofisticação. Com uma visão inovadora e um compromisso em oferecer vinhos que conquistem os paladares mais exigentes, a empresa tem alcançado resultados notáveis no mercado de exportação.")
    st.write("Neste contexto, investir na VitiBrasil significa apostar em uma marca consolidada, com um histórico comprovado de sucesso nas exportações de vinhos. Além disso, a empresa possui uma estrutura sólida e uma equipe experiente, pronta para impulsionar ainda mais seu crescimento e conquistar novos mercados.")
    st.subheader("Crescimento")
    st.write("Nos últimos anos, a VitiBrasil tem experimentado um crescimento notável e consistente em suas exportações de vinhos. Essa trajetória ascendente é resultado de uma combinação de fatores estratégicos e diferenciais competitivos que impulsionaram a marca a conquistar novos mercados e aumentar sua presença global.")
    st.write("O sucesso da VitiBrasil nas exportações pode ser atribuído a diversos elementos-chave. Em primeiro lugar, a empresa investiu na expansão de sua capacidade produtiva, modernizando suas instalações e adotando tecnologias de ponta para otimizar a produção de vinhos de alta qualidade em larga escala. Esse investimento estratégico permitiu à VitiBrasil atender à crescente demanda internacional e garantir o fornecimento consistente de seus produtos.")
    st.subheader("Perspectiva Futura")
    st.write("As perspectivas futuras da VitiBrasil são promissoras e oferecem um horizonte repleto de oportunidades para investidores. A VitiBrasil também está explorando novos mercados emergentes e fortalecendo sua presença em regiões onde já é reconhecida.")
    
if __name__ == '__main__':
    main()


def apply_custom_style():
    st_custom_style = """
                <style>
                summary {
                    display: none;
                }
                h2 {
                    color: {prim-color};
                }
                header[data-testid="stHeader"] {
                    background-image: linear-gradient({prim-color}, {prim-color}, purple);
                }
                div[data-testid="stStatusWidget"] div div div svg{
                    color: white;
                }
                #relat-rio-de-exporta-o-de-vinhos, #tabela-resumida-com-informa-es-de-exporta-es-nos-ltimos-anos{
                    text-align:center;
                }
                div[data-testid="stStatusWidget"] img{
                    opacity: 100%;
                }
                div[data-testid="stStatusWidget"] label{
                    color: white;
                }
                div[data-testid="stStatusWidget"] button{
                    color: white;
                    background: #9e829b;
                    border-radius: 20px;
                }
                #MainMenu{
                    color: white;
                    visibility: hidden;
                }
                * {
                  -webkit-user-drag: none;
                  -khtml-user-drag: none;
                  -moz-user-drag: none;
                  -o-user-drag: none;
                  user-drag: none;
                }
                a[href="#hide"] {
                    visibility: hidden;
                }
                div[data-testid="stDecoration"] {
                    background-image: none;
                    background-color: black;
                }
                section>div.block-container {
                    padding-top: 60px;
                }
                thead tr th:first-child {
                    display:none
                }
                tbody th {
                    display:none
                }
                .stAlert a {
                    display: none;
                }
                button[role="tab"][aria-selected="true"] {
                    background: #9e829b;
                    padding: 4px;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    color: white;
                }
                div[data-testid="collapsedControl"] {
                    color: white;
                }
                [tabindex="0"] > * {
                
                    max-width: 86rem !important;
                }
                #grupo {
                    background: #9e829b;
                    padding: 15px;
                    border-radius: 10px;
                }
                </style>
                """.replace('{prim-color}', PRIMARY_COLOR)
    st.markdown(st_custom_style, unsafe_allow_html=True)
    

apply_custom_style()

# Configurations in Streamlit

# Read Dataframes
df_exp_vinho     = pd.read_csv('datasets/tech-challenge/content/ExpVinho.csv', delimiter=";")

# Tratamento Dados Exportação
df_exp_vinho.drop(columns=['Id'], inplace=True)
df_exp_vinho.set_index("País", inplace=True)

colunas = df_exp_vinho.columns[-30:]
#colunas = colunas.insert(0, df_exp_vinho.columns[0])
df_exp_vinho = df_exp_vinho[colunas]

new_columns_name = []
for col in df_exp_vinho.columns:
    if str(col) == 'País':
        new_columns_name.append(col)
        
    if str(col).endswith(".1"):
        new_columns_name.append(str(col).replace(".1", " US$"))
        
    elif not str(col).endswith(".1") and not str(col) == "País":
        new_columns_name.append(str(col).replace(".1", " US$"))

df_exp_vinho.columns = new_columns_name

for idx, row in df_exp_vinho.iterrows():
    df_exp_vinho.loc[df_exp_vinho.index == idx, "Total em Litros"] = row[0::2].sum()

for idx, row in df_exp_vinho.iterrows():
    df_exp_vinho.loc[df_exp_vinho.index == idx, "Total em US$"] = row[1::2].sum()
    
df_exp_vinho_litros = df_exp_vinho.copy()
    
df_exp_vinho_litros_resumida = df_exp_vinho_litros[df_exp_vinho_litros.columns[-2:]]
df_exp_vinho_litros_resumida['Total em US$'] = df_exp_vinho_litros_resumida['Total em US$'].astype(float)

####### TABELA RESUMIDA GERAL #######
st.subheader("Base de dados Utilizada para a Análise")
st.write("Nos últimos 15 anos, a VitiBrasil alcançou um crescimento notável em suas exportações de vinhos, conquistando mercados em diversos países ao redor do mundo. Durante esse período, alguns países se destacaram como destinos-chave para os vinhos da VitiBrasil.")
st.write("Os Estados Unidos emergiram como um dos principais mercados para as exportações da VitiBrasil. Com sua enorme base de consumidores e uma crescente apreciação por vinhos de qualidade, os Estados Unidos têm sido um mercado estratégico para a empresa. Através de parcerias com importadores e distribuidores locais, a VitiBrasil conseguiu aumentar sua presença e expandir sua participação de mercado nesse país.")
st.write("Além disso, o mercado europeu desempenhou um papel significativo nas exportações da vinícola. Países como Rússia, Reino Unido, Alemanha e França se destacaram como destinos importantes para os vinhos da empresa. A Europa, conhecida por sua tradição vitivinícola, tem apreciado a qualidade e a diversidade dos vinhos da VitiBrasil, abrindo portas para uma presença cada vez maior da empresa nesse continente.")
df_exp_vinho_litros_resumida1 = df_exp_vinho_litros_resumida.reset_index()
builder = GridOptionsBuilder.from_dataframe(df_exp_vinho_litros_resumida1)
builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=7)
gol                        = builder.build()
AgGrid(df_exp_vinho_litros_resumida1, gridOptions=gol)


############### Visualização Top 15 Países ###############
st.write('')
tab1, tab2, tab3, tab4 = st.tabs(["📊 Principais Exportadores", "📊 Exportações Gerais", "📊 Mercados", "📜 Informações do Projeto"])

with tab1:
    st.write('')
    st.subheader("Lucro Obtido nos Últimos 15 Anos")
    st.write("Ao analisar as tendências e padrões dos países que mais geraram lucro para o Brasil nos últimos 15 anos podemos oferecer uma visão estratégica valiosa para potenciais investidores. Durante esse período, o Brasil estabeleceu relações econômicas sólidas com países-chave, como os Estados Unidos, a China, a Alemanha, o Reino Unido e os Países Baixos. Essas nações se destacaram como parceiros comerciais consistentes, contribuindo significativamente para a economia brasileira. Por outro lado, o Paraguai emergiu como um mercado promissor na importação de vinhos brasileiros. Embora seja um país vizinho, sua demanda crescente por vinhos de qualidade tem criado oportunidades atrativas para investidores interessados nesse setor. A proximidade geográfica e a relação comercial entre o Brasil e o Paraguai fornecem uma base sólida para o intercâmbio comercial, com o Paraguai se tornando um destino estratégico para as exportações de vinhos brasileiros.")
    st.write("Essa combinação de fatores oferece um cenário favorável para investidores que buscam explorar o potencial do mercado de vinhos no Brasil e no Paraguai. Os Estados Unidos, a China e o Reino Unido, como importantes parceiros comerciais do Brasil, representam oportunidades sólidas para expandir as exportações de vinhos brasileiros e estabelecer parcerias duradouras. Além disso, o crescente interesse do Paraguai na importação de vinhos brasileiros destaca o potencial de negócios no mercado regional. Investir na produção e exportação de vinhos de qualidade, adaptados às preferências do consumidor paraguaio, pode proporcionar um crescimento significativo no lucro gerado para o Brasil.")
    st.write("Essa análise conjunta ressalta a importância estratégica desses países como destinos para investimentos no setor de vinhos. A diversificação das exportações de vinhos brasileiros, atendendo às demandas dos mercados estabelecidos e explorando o potencial de novos mercados como o Paraguai, pode fortalecer a posição competitiva do Brasil no cenário global de vinhos. Portanto, para investidores interessados em explorar oportunidades no setor de vinhos, a análise dos países que mais geraram lucro para o Brasil e a relevância do mercado paraguaio como importador de vinhos brasileiros fornecem uma base sólida para avaliar o potencial de investimento. O Brasil apresenta uma oferta diversificada e de qualidade, com mercados estabelecidos e em crescimento, permitindo uma entrada estratégica e rentável nesse segmento de negócio.")
    df_exp_vinho_maiores_lucros = df_exp_vinho_litros.sort_values(by='Total em US$', ascending=False)
    cols = df_exp_vinho_maiores_lucros.columns[1::2]
    df_exp_vinho_maiores_lucros = df_exp_vinho_maiores_lucros[cols]
    #st.write(df_exp_vinho_maiores_lucros)
    df_sample = df_exp_vinho_maiores_lucros.head(15)
    df_sample.drop(columns='Total em US$', inplace=True)
    df_sample = df_sample.T
    fig = go.Figure()
    exec = 0
    for list in df_sample.T.values.tolist():
        fig.add_trace(go.Scatter(x=df_sample.index, y=list, name=df_sample.columns[exec]))
        exec +=1    

    fig.update_layout(autosize=False, width=1300, height=500)
    st.plotly_chart(fig)
    
    st.write('')
    st.subheader("Comparativo de Litros Exportados e Lucro Obtido nos Últimos 15 Anos")
    st.write("A análise comparativa entre o total de litros de vinho exportados e o total de dólares gerados com as exportações de vinho no Brasil é de grande relevância para os investidores que desejam entender e avaliar o potencial de investimento nesse setor. Ao examinar esses dados nos últimos anos, é possível obter insights sobre a eficiência e o valor agregado das exportações de vinho brasileiro. A análise revela uma relação complexa entre a quantidade de litros exportados e o valor em dólares gerado.")
    st.write("É importante ressaltar que apenas o volume de litros de vinho exportados não é um indicador definitivo do sucesso das exportações. A qualidade, a diversidade e a segmentação dos mercados de destino têm um impacto significativo nos resultados financeiros. Em alguns casos, pode ser observado que um grande volume de litros de vinho é exportado, mas o valor em dólares gerado é relativamente baixo. Isso pode sugerir a necessidade de ajustes estratégicos, como a identificação de segmentos de mercado mais lucrativos e o aprimoramento da qualidade e imagem dos vinhos brasileiros para atender às preferências desses consumidores. Por outro lado, é possível identificar situações em que um volume menor de litros de vinho exportados resulta em um valor mais alto em dólares. Isso pode indicar a conquista de mercados de maior poder aquisitivo, a oferta de vinhos premium com preços mais elevados e uma estratégia de marketing eficiente.")
    st.write("Essa análise comparativa fornece uma visão estratégica para os investidores que desejam avaliar o potencial de investimento no setor de vinhos brasileiros. Ela permite identificar oportunidades para otimizar tanto a quantidade quanto o valor das exportações, por meio de estratégias como a conquista de mercados mais rentáveis, o aprimoramento da qualidade e a criação de uma imagem de marca sólida. Além disso, a análise comparativa pode ajudar os investidores a entender as dinâmicas do mercado global de vinhos, identificar tendências de consumo e antecipar demandas futuras. Isso permite que tomem decisões informadas e estratégicas, direcionando recursos para áreas com maior potencial de retorno financeiro.")
    df_exp_vinho_litros1 = df_exp_vinho_litros.sort_values(by='Total em US$', ascending=False)
    df_exp_vinho_litros1 = df_exp_vinho_litros1.head(15)
    v0 = df_exp_vinho_litros1[df_exp_vinho_litros1.columns[1::2][:-1]].sum().values.tolist()
    v1 = df_exp_vinho_litros1[df_exp_vinho_litros1.columns[0::2][:-1]].sum().values.tolist()

    fig = go.Figure(data=[
        go.Bar(name="Total em US$", x=df_exp_vinho_litros.columns[0::2][:-1], y=v0, marker_color='indianred'),
        go.Bar(name="Total em Litros(Kg)", x=df_exp_vinho_litros.columns[0::2][:-1], y=v1, marker_color='lightsalmon')
    ])
    
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=1300, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    st.plotly_chart(fig)
    
    ####### GRÁFICO DE % DOS PAISES QUE MAIS FATURARAM #######
    st.subheader('Porcentagem dos 15 paises que mais faturaram para o Brasil em Dólar')
    st.write("Ao observar o gráfico, podemos identificar os 15 principais países que se destacaram na contribuição para o faturamento da VitiBrasil. Esses países têm desempenhado um papel crucial no sucesso das exportações da empresa e no fortalecimento da presença do vinho brasileiro nos mercados internacionais. Os dados percentuais fornecidos no gráfico demonstram a proporção do faturamento que os países representam. Isso permite avaliar a relevância relativa de cada mercado para a VitiBrasil e identificar as principais fontes de receita.")
    col1, col2 = st.columns(2)
    col2.write("Dentre os 15 países, é possível que alguns tenham contribuído com uma porcentagem significativamente maior do faturamento total, indicando uma maior dependência da VitiBrasil desses mercados específicos. Por outro lado, outros países podem ter uma participação menor, mas ainda assim desempenham um papel importante como mercados em crescimento ou como nichos estratégicos. Essa análise percentual é valiosa para a VitiBrasil e seus investidores, pois permite que ambos identifique seus principais mercados-alvo e concentre esforços para atender às demandas desses países de maneira eficaz. Além disso, a empresa pode identificar oportunidades de expansão em mercados com uma participação menor, mas com potencial de crescimento.")
    col2.write("É importante ressaltar que a dinâmica do mercado de vinhos é fluida, com mudanças nas preferências dos consumidores, flutuações econômicas e fatores políticos que podem influenciar as exportações. Portanto, a VitiBrasil deve monitorar essas tendências e ajustar suas estratégias de acordo para garantir um crescimento sustentável e a manutenção de relacionamentos sólidos com os principais países compradores.")
    df_exp_vinho_litros_resumida1 = df_exp_vinho_litros_resumida.reset_index()
    df_porc_p15 = analise.grafico_pie_p15(df_exp_vinho_litros_resumida1)
    fig = go.Figure()
    fig.add_pie(labels=df_porc_p15['grupo'], values=df_porc_p15['total_dolares'], marker_colors=["indianred", "lightsalmon"])
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
    ))
    col1.plotly_chart(fig)
    

    ###### GRAFICO DE LINHA DOS PAISES POR NIVEL SOCIOECONIMO ######
    st.write('')
    st.subheader('Tendência de Exportação em Dólar por Nível Socioeconômico')
    st.write("1. Países Desenvolvidos: Os países desenvolvidos são tradicionalmente grandes importadores e consumidores de vinhos de alta qualidade. Nações como Estados Unidos, Canadá, Reino Unido, Alemanha, França e Austrália têm uma cultura enraizada de apreciação do vinho e consumidores dispostos a pagar preços mais elevados por produtos premium. Esses países possuem uma demanda estabelecida por vinhos de diferentes regiões produtoras, tanto do Novo Mundo como do Velho Mundo. A tendência de consumo elevado tem impulsionado a importação de vinhos de prestígio e exclusivos.")
    st.write("2. Países Subdesenvolvidos: Os países subdesenvolvidos geralmente enfrentam desafios econômicos e infraestruturais que limitam sua participação no mercado global de exportação de vinhos. No entanto, alguns países em desenvolvimento têm conseguido superar esses desafios e se estabelecer como produtores e exportadores de vinhos competitivos. Países como Argentina, Chile, Uruguai e Brasil têm investido na indústria vitivinícola, aproveitando seus recursos naturais e adotando práticas avançadas de vinificação. Essas nações têm visto um aumento na exportação de vinhos de qualidade a preços mais acessíveis, alcançando mercados regionais e globais.")
    st.write("3. Países Emergentes: Os países emergentes estão se tornando cada vez mais importantes no mercado global de exportação de vinhos. Países como África do Sul, China, Índia e México têm experimentado um crescimento significativo no consumo e importação de vinhos. À medida que esses países passam por um rápido desenvolvimento socioeconômico, a classe média está se expandindo, o poder aquisitivo está aumentando e o interesse por produtos de qualidade, incluindo vinhos, está crescendo. Isso tem impulsionado a importação de vinhos de diferentes origens e estilos, bem como o desenvolvimento de vinícolas locais para atender à demanda crescente.")
    st.write("Em resumo, a tendência de exportação de vinhos varia de acordo com o nível socioeconômico dos países. Países desenvolvidos são grandes importadores e consumidores de vinhos de alta qualidade. Países subdesenvolvidos estão conseguindo superar desafios para se estabelecer como produtores e exportadores competitivos. Países emergentes estão experimentando um rápido crescimento no consumo e importação de vinhos, impulsionados pelo desenvolvimento socioeconômico e aumento do poder aquisitivo. Essas tendências refletem as diferentes dinâmicas e oportunidades em cada nível socioeconômico.")
    df_p15 = analise.grafico_line_p15_by_socio(df_exp_vinho_maiores_lucros)
    # Para renderizar é preciso ser esse df -> df_p15.iloc[:,:-1].T
    df_p15 = df_p15.iloc[:,:-1]
    #st.write(df_p15.values.tolist())
    
    fig = go.Figure()
    exec = 0
    for list in df_p15.values.tolist():
        fig.add_trace(go.Scatter(x=df_p15.columns, y=list, name=df_p15.index[exec]))
        exec +=1    
    
    fig.update_layout(autosize=False, width=1300, height=500)
    st.plotly_chart(fig)
    
    ####### TABELA DE COMPARAÇÃO DOS PAISES QUE MAIS CONSOMEM COM A GPD #######
    # st.subheader('Comparação dos paises que mais consomem com a o GPD')
    # df_p15 = analise.df_gdp(df_exp_vinho_maiores_lucros)
    # st.dataframe(df_p15)

    ###### GRAFICO DE BARRAS DA QTD DE PAISES POR NIVEL SOCIOECONOMICO ######
    col1, col2 = st.columns(2)
    df_p15 = analise.grafico_bar_p15_qtde_by_socio(df_exp_vinho_maiores_lucros)

    fig = go.Figure(data=[
        #go.Bar(name="Total em US$", x=df_exp_vinho_litros.columns[0::2][:-1], y=v0, marker_color='indianred'),
        go.Bar(name="Total paises", x=df_p15.index, y=df_p15, marker_color=['lightsalmon','indianred', 'lightsalmon'])
    ])
    
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=500, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    col1.subheader("Quantidade de Paises por Nível Socioeconômico")
    col1.plotly_chart(fig)
    
    ####### GRÁFICO DE BARRAS DAS QUESTÕES SOCIOECONOMICAS #######
    df_p15 = analise.grafico_bar_p15_by_socio(df_exp_vinho_maiores_lucros)
    fig = go.Figure(data=[
        #go.Bar(name="Total em US$", x=df_exp_vinho_litros.columns[0::2][:-1], y=v0, marker_color='indianred'),
        go.Bar(name="Total paises", x=df_p15.index, y=df_p15['Total em US$'], marker_color=['lightsalmon','indianred', 'lightsalmon'])
    ])
    
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=600, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    col2.subheader("Valores em Dólar por Nível Socioeconômico")
    col2.plotly_chart(fig)
    
    
with tab2: 
    st.write('')
    ####### GRÁFICO DE MAPA GERAL #######
    df_exp_vinho_litros_mapa = df_exp_vinho_litros.copy()
    df_exp_vinho_litros_mapa = df_exp_vinho_litros_mapa[df_exp_vinho_litros_mapa.columns[0::2][:-1]]
    
    paises =  pd.read_json('assets/iso_paises.json', lines=True)
    df_exp_vinho_litros_mapa['ISO ALPHA'] = ''
    for _, row in paises.iterrows():
        df_exp_vinho_litros_mapa.loc[df_exp_vinho_litros_mapa.index.str.contains(row['nome']), 'ISO ALPHA'] = row['alpha-3']
    
    pais  = []
    ano   = []
    valor = []
    iso   = []
    
    for pais_name, row  in df_exp_vinho_litros_mapa.iterrows():
        ano_start = 2007
        for _ in range(0, 15):
            pais.append(pais_name)
            ano.append(ano_start)
            valor.append(row[f'{ano_start}'])
            iso.append(row['ISO ALPHA'])
            ano_start += 1
            
    st.subheader("Litros Exportados nos Últimos 15 anos")
    st.write("Nos últimos 15 anos, a VitiBrasil, uma das principais empresas produtoras de vinho do Brasil, tem se destacado no mercado internacional, exportando uma quantidade significativa de litros para diversos países ao redor do mundo. Durante esse período, vários países se destacaram como principais destinos das exportações da VitiBrasil. ")
    st.write("Entre os principais países que receberam os litros de vinho brasileiro da VitiBrasil, podemos citar:")
    st.write("1. Estados Unidos: Os Estados Unidos se tornaram um mercado importante para a VitiBrasil nos últimos anos. Com uma demanda crescente por vinhos de qualidade, os consumidores americanos têm apreciado cada vez mais os produtos da VitiBrasil, o que resultou em um aumento significativo nas exportações de litros para esse país.")
    st.write("2. Paraguai: O Paraguai tem se destacado como um mercado promissor para os vinhos brasileiros. A VitiBrasil tem aproveitado essa oportunidade, exportando litros de vinho para o país. O interesse crescente dos consumidores paraguaios pelos vinhos brasileiros tem contribuído para o aumento das exportações ao longo dos anos.")
    st.write("3. Alemanha: A Alemanha é conhecida por sua cultura do vinho e seu alto padrão de qualidade. A VitiBrasil encontrou um nicho nesse mercado exigente, exportando litros de vinho para a Alemanha. A reputação da VitiBrasil tem se fortalecido entre os apreciadores de vinho alemães, resultando em um aumento nas exportações ao longo dos anos.")
    st.write("4. China: O mercado chinês tem se tornado cada vez mais relevante para a indústria vinícola global. A VitiBrasil tem aproveitado essa oportunidade, exportando litros de vinho para a China. O interesse crescente dos consumidores chineses pelos vinhos brasileiros tem contribuído para o aumento das exportações.")
    st.write("Além desses países mencionados, a VitiBrasil também tem exportado litros de vinho para outros destinos ao redor do mundo, como Rússia, Japão, Reino Unido e outros países da Europa e da América do Sul. Essa diversificação de mercados tem sido fundamental para o crescimento das exportações da VitiBrasil nos últimos 15 anos. Essa expansão das exportações da VitiBrasil reflete a qualidade e a competitividade dos vinhos brasileiros no cenário internacional. A empresa tem investido em tecnologia, sustentabilidade e aprimoramento da produção para atender às exigências dos mercados internacionais e consolidar sua posição como uma referência na indústria vitivinícola brasileira.")

    df_mapa = pd.DataFrame({"País": pais, "Ano": ano, "Litros(KG)": valor, "ISO Alpha": iso})
    fig = px.choropleth(df_mapa, locations='ISO Alpha', color='Litros(KG)', hover_name='País',
                        projection='eckert4', animation_frame='Ano',color_continuous_scale=[[0, 'rgb(240,240,240)'],
                      [0, 'rgb(255,255,255)'],
                      [0.25, 'rgb(161,119,155)'],
                      [0.5, 'rgb(139,95,133)'],
                      [0.75, 'rgb(107,62,101)'],
                      [1, 'rgb(87,43, 82)']],
                        title='GDP per Capita by Country')
    
    
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C',
                                          landcolor='rgba(51,17,0,0.2)',
                                          subunitcolor='grey'),
                                  title = '',font = {"size": 13, "color":"White"},titlefont = {"size": 25, "color":"White"},
                                  geo_scope='world', margin={"r":0,"t":40,"l":0,"b":0}, plot_bgcolor='#4E5D6C', 
                                  width=1300, height=600)
    st.plotly_chart(fig)
     
    ####### GRÁFICO DE LINHA % ANUAL GERAL #######
    st.write('')
    st.subheader("Crescimento x Perda nas exportações de vinho nos últimos anos")
    st.write("O gráfico em questão apresenta o crescimento e a perda das exportações da VitiBrasil, uma das principais empresas produtoras de vinho do Brasil, nos últimos anos. Essa representação visual é valiosa para compreender a evolução das exportações da empresa e analisar seu desempenho no mercado internacional.")
    st.write("Ao observar o gráfico, podemos identificar diferentes períodos de crescimento e perda ao longo dos anos. É importante destacar que os fatores que impulsionam ou afetam as exportações podem variar, incluindo mudanças nas condições econômicas globais, flutuações cambiais, políticas comerciais, demanda dos consumidores e até mesmo eventos específicos que possam impactar o mercado de vinhos. Durante alguns períodos, podemos notar um crescimento acentuado nas exportações da VitiBrasil. Esses momentos de crescimento podem ser resultado de estratégias de expansão em novos mercados, investimentos em marketing e promoção da marca, melhorias na qualidade dos vinhos ou até mesmo o reconhecimento internacional dos produtos da empresa.")
    st.write("Por outro lado, é possível observar períodos de perda nas exportações. Essas quedas podem ocorrer devido a fatores externos, como crises econômicas, flutuações nas demandas dos mercados internacionais, concorrência acirrada de outros produtores de vinho ou desafios logísticos na cadeia de suprimentos. Identificar as causas dessas perdas pode ser crucial para a empresa ajustar suas estratégias e mitigar riscos futuros. É importante ressaltar que as flutuações nas exportações são comuns no mercado global de vinhos e em qualquer indústria. Portanto, é fundamental que a VitiBrasil esteja preparada para se adaptar às mudanças do mercado, diversificar seus mercados de exportação e continuar aprimorando seus produtos e serviços para se manter competitiva no cenário internacional.")
    st.write("Ao analisar o gráfico de crescimento versus perda das exportações da VitiBrasil nos últimos anos, a empresa e seus investidores conseguem obter insights valiosos para orientar suas estratégias futuras. Isso inclui identificar oportunidades de crescimento, otimizar suas operações, fortalecer relacionamentos com parceiros comerciais, investir em inovação e garantir a qualidade e a consistência de seus produtos.")
    df_exp_vinho_litros1 = df_exp_vinho_litros.sort_values(by='Total em US$', ascending=False)
    df_exp_vinho_litros1 = df_exp_vinho_litros1
    df_dolar_resumida  = df_exp_vinho_litros1[df_exp_vinho_litros1.columns[1::2][:-1]]
    df_vinhos_resumida = df_exp_vinho_litros1[df_exp_vinho_litros1.columns[0::2][:-1]]
    
    year = [x for x in range(2007, 2022)]
    df_dolar_resumida = pd.DataFrame({'Ano': year, 'Total em US$': df_dolar_resumida.sum().values})
    df_dolar_resumida['Ano'] = df_dolar_resumida['Ano'].astype(str)
    df_dolar_resumida['Total em US$'] = df_dolar_resumida['Total em US$'].astype(float)
    
    df_vinhos_resumida = pd.DataFrame({'Ano': year, 'Total em Litros': df_vinhos_resumida.sum().values})
    df_vinhos_resumida['Ano'] = df_vinhos_resumida['Ano'].astype(str)
    df_vinhos_resumida['Total em Litros'] = df_vinhos_resumida['Total em Litros'].astype(float)
    
    df_dolar_resumida['percentual'] = ''
    df_vinhos_resumida['percentual'] = ''
    
    result = []
    for _, row in df_dolar_resumida.iterrows():
        v1 = df_dolar_resumida.loc[df_dolar_resumida['Ano'] == f'{row["Ano"]}']
        v2 = df_dolar_resumida.loc[df_dolar_resumida['Ano'] == f'{int(row["Ano"]) +1}']
        result.append(((v2['Total em US$'].values - v1['Total em US$'].values) / v1['Total em US$'].values) * 100)
    result2 = []
    for value in result[:-1]:
        result2.append(round(value[0],2))
    result2.insert(0, 0)
    
    result = []
    for _, row in df_vinhos_resumida.iterrows():
        v1 = df_vinhos_resumida.loc[df_vinhos_resumida['Ano'] == f'{row["Ano"]}']
        v2 = df_vinhos_resumida.loc[df_vinhos_resumida['Ano'] == f'{int(row["Ano"]) +1}']
        result.append(((v2['Total em Litros'].values - v1['Total em Litros'].values) / v1['Total em Litros'].values) * 100)
    result3 = []
    for value in result[:-1]:
        result3.append(round(value[0],2))
    result3.insert(0, 0)
    
    fig = go.Figure()
    
    text1 = [str(value)+"%" for value in result2]
    text2 = [str(value)+"%" for value in result3]
    fig.add_trace(go.Scatter(x=year, y=result2, name='Total em US$',text=text1, marker_color='indianred', mode='lines+markers+text'))
    fig.add_trace(go.Scatter(x=year, y=result3, name='Total em Litros',text=text2, marker_color='lightsalmon', mode='lines+markers+text'))
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)
    fig.update_layout(autosize=False, width=1300, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    
    st.plotly_chart(fig)

    ####### GRÁFICO DE LINHA DOS CONTINENTES #######
    st.subheader("Tendência de Exportação em Cada Continente")
    st.write("1. África: A África tem emergido como um continente promissor na produção de vinhos e, consequentemente, na exportação desses produtos. Países como África do Sul, Marrocos e Argélia têm investido na indústria vinícola e ganhado reconhecimento internacional por seus vinhos de alta qualidade. A exportação de vinhos africanos tem apresentado uma tendência crescente, impulsionada pela expansão da demanda global por vinhos exóticos e distintos. Esses países têm aproveitado a oportunidade para posicionar-se como produtores de vinhos premium, diversificando sua oferta e explorando mercados internacionais em busca de crescimento.")
    st.write("2. América: A América é um continente com uma tradição estabelecida na produção de vinhos e uma forte presença no mercado de exportação. Países como Estados Unidos, Argentina, Chile e Brasil são conhecidos por sua produção e exportação de vinhos de alta qualidade. Os Estados Unidos, em particular, têm experimentado um crescimento significativo na exportação de vinhos nos últimos anos, impulsionado pelo aumento do consumo interno e pela crescente demanda global por vinhos americanos. A América Latina, com seu clima favorável e terroirs diversificados, tem se destacado na produção de vinhos finos e ganhado reconhecimento internacional.")
    st.write("3. Ásia: Embora a produção de vinhos na Ásia seja relativamente recente, o continente tem demonstrado um crescimento expressivo na exportação de vinhos nos últimos anos. Países como China, Japão e Índia estão investindo na indústria vitivinícola e buscando aumentar sua presença no mercado global de vinhos. A crescente classe média asiática, juntamente com um maior interesse pelo consumo de vinhos, impulsionou a demanda interna e a exportação de vinhos asiáticos. A China, em particular, tem se destacado como um mercado em rápido crescimento e também como produtor de vinhos de qualidade. Essa tendência indica um potencial significativo para o crescimento contínuo da exportação de vinhos asiáticos.")
    st.write("4. Europa: A Europa é tradicionalmente reconhecida como uma região líder na produção e exportação de vinhos. Países como França, Itália, Espanha e Portugal são conhecidos por sua rica tradição vinícola e por produzirem alguns dos melhores vinhos do mundo. A exportação de vinhos europeus continua a desempenhar um papel importante no mercado global, com os países europeus consolidando sua posição como fornecedores confiáveis de vinhos de alta qualidade. A diversidade de estilos, terroirs e variedades de uva oferecidas pela Europa contribui para sua atratividade no mercado de exportação de vinhos.")
    st.write("Em resumo, a tendência de exportação de vinhos varia em cada continente. A África está emergindo como uma nova região de exportação, a América e a Europa têm uma posição estabelecida como líderes na exportação de vinhos, e a Ásia está experimentando um rápido crescimento nesse mercado. Essas tendências refletem o desenvolvimento da indústria vitivinícola em cada continente e as preferências em constante evolução dos consumidores em todo o mundo.")
    df_exp_vinho_maiores_lucros = df_exp_vinho_litros.sort_values(by='Total em US$', ascending=False)
    cols = df_exp_vinho_maiores_lucros.columns[1::2][-16:]
    df_exp_vinho_maiores_lucros = df_exp_vinho_maiores_lucros[cols]

    df_p15 = analise.grafico_line_p15_by_regiao(df_exp_vinho_maiores_lucros)
    fig = go.Figure()
    exec = 0
    for list in df_p15.values.tolist():
        fig.add_trace(go.Scatter(x=df_p15.columns, y=list, name=df_p15.index[exec]))
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        exec +=1    
    
    fig.update_layout(autosize=False, width=1300, height=500)
    st.plotly_chart(fig)
    
    ####### GRÁFICO DE TOTAL DE IMPORTAÇÃO EM DOLAR #######
    st.subheader('Total de Importação em dólar dos continentes')
    st.write("O gráfico em questão apresenta o total de importação em dólar dos continentes África, América, Ásia e Europa. Essa visualização permite uma comparação entre as importações dessas regiões e fornece insights sobre as dinâmicas do comércio internacional.")
    st.write("Ao analisar o gráfico, podemos observar que tanto a Europa quanto a América possuem valores quase iguais de importação em dólar. Isso indica que esses dois continentes têm uma participação significativa nas importações globais e são importantes destinos de bens e serviços provenientes de outras regiões. No entanto, apesar de ter valores semelhantes à América, a Europa continua sendo a maior importadora dos quatro continentes. Isso pode ser resultado de uma economia robusta, uma ampla base industrial, uma extensa rede de acordos comerciais e uma demanda diversificada por produtos importados.")
    st.write("Por outro lado, a Ásia e a África são as regiões com os menores valores de importação em dólar. Isso pode refletir diferentes fatores, como economias emergentes, infraestrutura comercial menos desenvolvida, dependência de recursos naturais ou uma base industrial menos diversificada. Essas características podem limitar a capacidade dessas regiões de importar grandes volumes de bens e serviços.")
    st.write("Em resumo, o gráfico do total de importação em dólar dos continentes África, América, Ásia e Europa revela a importância da Europa e da América como principais importadoras, com valores quase iguais. Enquanto isso, a Ásia e a África mostram valores menores, com a África ocupando a posição de menor importador. Essa análise pode fornecer insights sobre as dinâmicas do comércio internacional e auxiliar na elaboração de estratégias comerciais eficazes para cada continente.")
    s_p15_regiao = analise.grafico_bar_p15_by_regiao(df_exp_vinho_litros_resumida1)
    fig = go.Figure(data=[
        go.Bar(name="Total em US$", x=s_p15_regiao.index, y=s_p15_regiao, marker_color='indianred'),
    ])
    
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=1300, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    st.plotly_chart(fig)
    
with tab3:
    st.write('')
    ####### MERCOSUL ################
    st.subheader('Análise da importação de vinhos Brasileiros pelos Países do Mercosul')
    st.write("O Mercosul, também conhecido como Mercado Comum do Sul, é uma organização regional que busca promover a integração econômica e política entre países da América do Sul. Atualmente, os membros plenos do Mercosul são Argentina, Brasil, Paraguai e Uruguai. A Venezuela, embora tenha se tornado membro pleno em 2012, está atualmente suspensa devido a preocupações com o cumprimento de suas obrigações internas. A Nova Zelândia e o México não fazem parte do Mercosul, portanto, não têm direito a voto nas decisões do bloco, por esse motivo esses países não constam no gráfico para análise.")
    st.write("Observando o gráfico, podemos notar que a Bolívia se destaca como o maior importador de vinhos brasileiros entre os países listados. Esse fato pode ser atribuído a diferentes motivos, como preferências de consumo, acordos comerciais e demanda crescente por vinhos brasileiros nesse mercado específico.")
    st.write("Além disso, é interessante notar que a Argentina, país vizinho do Brasil e conhecido por sua tradição vitivinícola, também figura como um dos principais importadores de vinhos brasileiros. Isso pode ser atribuído à proximidade geográfica e às relações comerciais estabelecidas entre os dois países.")
    st.write("O Uruguai, reconhecido por sua produção de vinhos de qualidade, também importa vinhos do Brasil, ocupando uma posição relevante no gráfico. Isso indica a busca por diversidade e complementaridade na oferta de vinhos, mesmo entre países que são concorrentes diretos na indústria vinícola.")
    st.write("Outros países como Chile, Colômbia, Peru, Suriname, Guiana e Equador também importam vinhos brasileiros, embora em volumes menores em comparação com os principais importadores. Esses mercados podem representar oportunidades de crescimento para a indústria vinícola brasileira, com potencial para expandir as exportações e conquistar consumidores nessas nações.")
    st.write("Em resumo, o gráfico da importação de vinhos do Brasil pelos países Bolívia, Uruguai, Argentina, Chile, Colômbia, Peru, Suriname, Guiana e Equador destaca a importância da Bolívia como o maior importador de vinhos brasileiros nesse conjunto de países. Mostra também a diversidade de mercados e a busca por diferentes características e sabores de vinhos por parte dos importadores. Esses dados podem ser úteis para a indústria vitivinícola brasileira ao identificar oportunidades de crescimento e estabelecer estratégias de expansão nessas nações.")
    
    st.write('Adicionar no fim do Projeto -  Fonte: https://mundoeducacao.uol.com.br/geografia/paisesmembros-mercosul.htm')
    df_mercosul = analise.grafico_bar_mercosul(df_exp_vinho_maiores_lucros)
    #st.dataframe(df_mercosul.iloc[:,-1:])
    fig = go.Figure(data=[
        #go.Bar(name="Total em US$", x=df_exp_vinho_litros.columns[0::2][:-1], y=v0, marker_color='indianred'),
        go.Bar(name="Paises Mercosul", x=df_mercosul.index, y=df_mercosul['Total em US$'], marker_color='lightsalmon')
    ])
    
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=1300, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    st.plotly_chart(fig)

    ##### GRAFICO DOS CONTINENTES
    st.subheader('Análise da exportação de Vinho pelos Continentes nos últimos Anos')
    df_continentes = analise.grafico_bar_continentes(df_exp_vinho_maiores_lucros)
    st.write('A análise da exportação de vinhos pelos continentes da África, América, Ásia, Europa e Oceania, revela algumas tendências interessantes.')
    st.write("1. América: A exportação de vinhos da VitiBrasil para países americanos, como Estados Unidos, Canadá, Paraguai e Bolívia, é uma parte significativa do mercado. A proximidade geográfica e a presença de consumidores sofisticados e conhecedores de vinho na região podem impulsionar o comércio bilateral.")
    st.write("2. Europa: A Europa é um mercado tradicionalmente importante para a indústria vinícola e a exportação de vinhos da VitiBrasil para países europeus, como Rússia, Alemanha e Reino Unido, pode representar uma oportunidade de alcance de consumidores que valorizam a diversidade e a qualidade dos vinhos.")
    st.write("3. Ásia: A exportação de vinhos da VitiBrasil para países asiáticos, como China e Japão, está em crescimento. O aumento da renda, a influência ocidental e o interesse crescente pela cultura do vinho nesses países podem impulsionar a demanda por vinhos brasileiros.")
    st.write("4. África: Embora a exportação de vinhos da VitiBrasil para a África possa ser menor em comparação com outros continentes, o aumento da classe média e o desenvolvimento do turismo em alguns países africanos podem gerar demanda por vinhos brasileiros. Países como África do Sul, Nigéria e Angola têm potencial de mercado a ser explorado.")
    st.write("5. Oceania: A Oceania é o continente de menor destaque na exportação de vinhos da VitiBrasil. No entanto, países como Austrália e Nova Zelândia possuem uma forte tradição vinícola e, embora sejam concorrentes, podem oferecer oportunidades para vinhos brasileiros exclusivos e distintos.")
    st.write("É importante ressaltar que essas são apenas tendências gerais e que a demanda por vinhos pode variar de acordo com cada país dentro de cada continente. Estratégias personalizadas de marketing, distribuição e desenvolvimento de relacionamentos comerciais são essenciais para aproveitar ao máximo as oportunidades em cada mercado.")
    st.write(" ")
    #st.dataframe(df_continentes)
    series_continente = df_continentes.groupby('continente').sum()['Total em US$']

    opcoes = ['Todos']
    opcoes.extend(series_continente.index)
    select_box = st.selectbox('Selecione o continente', options=opcoes)
    if select_box=='Todos':
        fig = go.Figure(data=[
            #go.Bar(name="Total em US$", x=df_exp_vinho_litros.columns[0::2][:-1], y=v0, marker_color='indianred'),
            go.Bar(name="Total por continente", x=series_continente.index, y=series_continente, marker_color='lightsalmon')
        ])
    else:
        df_continente_selecionado = df_continentes.query('continente == @select_box')['Total em US$']
        fig = go.Figure(data=[
            #go.Bar(name="Total em US$", x=df_exp_vinho_litros.columns[0::2][:-1], y=v0, marker_color='indianred'),
            go.Bar(name="Total por continente", x=df_continente_selecionado.index, y=df_continente_selecionado, marker_color='lightsalmon')
        ])

    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=1300, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    st.plotly_chart(fig)
    
with tab4:
    st.subheader('Sobre')
    st.write('Projeto desenvolvido por Estudantes da FIAP - Pós Tech em Data Analytics.')
    st.write("")
    st.subheader("Referências")
    st.markdown('<a href="http://vitibrasil.cnpuv.embrapa.br/"><b>Base de Dados Vitti Brasil</b></a>', unsafe_allow_html=True)
    st.write("")
    st.subheader("Responsáveis")
    st.markdown("<li>Brendon Calazans</li><li>Gabriel Rosa</li><li>Marcelo Meirelles</li>", unsafe_allow_html=True)

    
