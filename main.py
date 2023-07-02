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
    st.header("Vitivinicultura Brasileira")
    st.subheader("Introdução")
    st.write("A VitiBrasil é uma vinícola de renome internacional, dedicada à produção de vinhos excepcionais, e tem o prazer de compartilhar seu sucesso nas exportações nos últimos anos. Com base em sua expertise, qualidade incomparável e compromisso com a excelência, a VitiBrasil se estabeleceu como uma das principais marcas de vinhos do Brasil. Neste texto, destacaremos o crescimento impressionante das exportações da VitiBrasil e os motivos pelos quais investir nessa vinícola promissora é uma oportunidade única.")
    st.write("Nos últimos anos, a VitiBrasil tem ganhado destaque no cenário internacional como uma produtora de vinhos de alta qualidade e sofisticação. Com uma visão inovadora e um compromisso em oferecer vinhos que conquistem os paladares mais exigentes, a empresa tem alcançado resultados notáveis no mercado de exportação.")
    st.write("Neste contexto, investir na VitiBrasil significa apostar em uma marca consolidada, com um histórico comprovado de sucesso nas exportações de vinhos. Além disso, a empresa possui uma estrutura sólida e uma equipe experiente, pronta para impulsionar ainda mais seu crescimento e conquistar novos mercados.")
    st.subheader("Qualidade")
    st.write("A VitiBrasil é conhecida por sua busca incessante pela qualidade em todos os aspectos da produção de vinhos. Desde a seleção meticulosa das uvas até a fermentação controlada e o envelhecimento cuidadoso, cada etapa é realizada com precisão e dedicação. Os resultados são vinhos de caráter único, aromas cativantes e sabores refinados, que atraem os paladares mais exigentes ao redor do mundo.")
    st.write("A vinícola aproveita as características únicas de seu terroir brasileiro, combinando a influência de climas variados, solos distintos e microclimas específicos para produzir vinhos de caráter singular. As uvas são cultivadas com o máximo cuidado e colhidas no momento ideal de maturação, garantindo que apenas as melhores frutas sejam utilizadas na produção de seus vinhos.")
    st.subheader("Crescimento")
    st.write("Nos últimos anos, a VitiBrasil tem experimentado um crescimento notável e consistente em suas exportações de vinhos. Essa trajetória ascendente é resultado de uma combinação de fatores estratégicos e diferenciais competitivos que impulsionaram a marca a conquistar novos mercados e aumentar sua presença global.")
    st.write("O sucesso da VitiBrasil nas exportações pode ser atribuído a diversos elementos-chave. Em primeiro lugar, a empresa investiu na expansão de sua capacidade produtiva, modernizando suas instalações e adotando tecnologias de ponta para otimizar a produção de vinhos de alta qualidade em larga escala. Esse investimento estratégico permitiu à VitiBrasil atender à crescente demanda internacional e garantir o fornecimento consistente de seus produtos.")
    st.subheader("Perspectiva Futura")
    st.write("As perspectivas futuras da VitiBrasil são promissoras e oferecem um horizonte repleto de oportunidades para investidores. Com base em seu histórico de crescimento nas exportações e na qualidade excepcional de seus vinhos, a empresa está bem posicionada para continuar conquistando novos mercados e fortalecer sua presença global.")
    st.write("A VitiBrasil também está explorando novos mercados emergentes e fortalecendo sua presença em regiões onde já é reconhecida. Com uma estratégia de expansão global bem definida, a empresa está conquistando gradualmente uma posição de destaque em diferentes países e continentes, diversificando sua base de consumidores e reduzindo a dependência de mercados específicos.")
    
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
add_selectbox = st.sidebar.selectbox(
    "Selecione o que deseja Visualizar:",
    ("Exportação", "Importação", "Exportação x Importação", "Comércio", "Produção", "Comércio x Produção")
)

st.title("Relatório de Exportação de Vinhos")
st.write(' ')

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

#df_exp_vinho_litros.set_index("País", inplace=True)

for idx, row in df_exp_vinho_litros.iterrows():
    df_exp_vinho_litros.loc[df_exp_vinho_litros.index == idx, "Total em Litros"] = row[0::2].sum()
    
for idx, row in df_exp_vinho_litros.iterrows():
    df_exp_vinho_litros.loc[df_exp_vinho_litros.index == idx, "Total em US$"] = row[1::2].sum()
    
df_exp_vinho_litros_resumida = df_exp_vinho_litros[df_exp_vinho_litros.columns[-2:]]
df_exp_vinho_litros_resumida['Total em US$'] = df_exp_vinho_litros_resumida['Total em US$'].astype(float)

# Visualização dos Dados Exportação

with st.expander("📊 Informações de Exportação Geral"):
    
    st.subheader("Tabela Resumida com Informações de Exportações nos Últimos 15 Anos")
    st.write("Nos últimos 15 anos, a VitiBrasil alcançou um crescimento notável em suas exportações de vinhos, conquistando mercados em diversos países ao redor do mundo. Durante esse período, alguns países se destacaram como destinos-chave para os vinhos da VitiBrasil.")
    st.write("Os Estados Unidos emergiram como um dos principais mercados para as exportações da VitiBrasil. Com sua enorme base de consumidores e uma crescente apreciação por vinhos de qualidade, os Estados Unidos têm sido um mercado estratégico para a empresa. Através de parcerias com importadores e distribuidores locais, a VitiBrasil conseguiu aumentar sua presença e expandir sua participação de mercado nesse país.")
    st.write("Além disso, o mercado europeu desempenhou um papel significativo nas exportações da vinícola. Países como Rússia, Reino Unido, Alemanha e França se destacaram como destinos importantes para os vinhos da empresa. A Europa, conhecida por sua tradição vitivinícola, tem apreciado a qualidade e a diversidade dos vinhos da VitiBrasil, abrindo portas para uma presença cada vez maior da empresa nesse continente.")
    df_exp_vinho_litros_resumida1 = df_exp_vinho_litros_resumida.reset_index()
    builder = GridOptionsBuilder.from_dataframe(df_exp_vinho_litros_resumida1)
    builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=7)
    gol                        = builder.build()
    AgGrid(df_exp_vinho_litros_resumida1, gridOptions=gol)

    
with st.expander(" Maiores Exportadores de Vinho"):
    #px.line()
    st.subheader("Linha do Tempo dos Países que mais geraram Lucro ao Brasil nos Últimos 15 Anos")
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
    
with st.expander("Exportações e Lucros do Brasil nos Últimos 15 anos"):
    st.subheader("Linha do Tempo dos Países que mais Exportaram e Geraram Lucro ao Brasil nos Últimos 15 Anos")
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
    
with st.expander("Grafico de Mapa"):
    df_exp_vinho_litros_mapa = df_exp_vinho_litros.copy()
    df_exp_vinho_litros_mapa = df_exp_vinho_litros_mapa[df_exp_vinho_litros_mapa.columns[0::2][:-1]]
    st.write("####COLOCAR O TEXTO EXPLICATIVO AQUI####")
    
    paises =  pd.read_json('assets/iso_paises.json', lines=True)
    df_exp_vinho_litros_mapa['ISO ALPHA'] = ''
    for _, row in paises.iterrows():
        df_exp_vinho_litros_mapa.loc[df_exp_vinho_litros_mapa.index.str.contains(row['nome']), 'ISO ALPHA'] = row['alpha-3']
    
    st.write(df_exp_vinho_litros_mapa.loc[df_exp_vinho_litros_mapa['ISO ALPHA'] == ''])
    
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

    df_mapa = pd.DataFrame({"País": pais, "Ano": ano, "Litros(KG)": valor, "ISO Alpha": iso})
    st.subheader("Litros Exportados nos Últimos 15 anos")
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
    

with st.expander("$ Vendido"):
    st.write('test')
    
    # plt.figure(figsize=(22,8))
    # plt.plot(df_sample.T.index, df_sample.T.values)
    # plt.legend(df_sample.T.columns[0:12])
    # plt.ticklabel_format(style='plain', axis='y')
    # plt.xticks(rotation=90)
    # #plt.axhline(y=df_sample.T.values.mean(), color='red', linestyle='--', linewidth=3, label='Avg')
    # plt.title("Linha do Tempo dos Países que mais exportaram vinho nos Últimos 15 anos")
    # st.write(plt.show())
    
    #graph = alt.Chart(df_exp_vinho).mark_boxplot().encode(y="Total em Litros").properties(width=500)
    
    # df_sample = df_exp_vinho_litros_resumida.loc[(df_exp_vinho_litros_resumida["Total em Litros"] > 100000) & (df_exp_vinho_litros_resumida["Total em Litros"] <= 1000000)].sort_values(by="Total em Litros", ascending=False)
    # plt.figure(figsize=(22,8))
    # x_axis = np.arange(len(df_sample.index))
    # plt.bar(x_axis - 0.2, df_sample[['Total em Litros']].T.sum().values,width=0.4, label = "Litros")
    # plt.bar(x_axis + 0.2, df_sample[['Total em US$']].T.sum().values,width=0.4,  label="Valor US$")
    # plt.ticklabel_format(style='plain', axis='y')
    # plt.xticks(x_axis, df_sample.index)
    # plt.xticks(rotation=90)
    # #plt.axhline(y=df_exportacao_geral_litros.sum().median(), color='red', linestyle='--', linewidth=3, label='Mediana')
    # #plt.axhline(y=df_exportacao_geral_litros.sum().mean(), color='blue', linestyle='--', linewidth=3, label='Média')
    # plt.title("Linha do Tempo de Exportação de Vinho e Lucro(US$) do Brasil nos Últimos 15 anos")
    # plt.legend();
    
## Gabriel Analise

with st.expander('Porcentagem dos 15 paises que mais faturaram para o Brasil em Dólar'):
    #st.dataframe(df_exp_vinho_litros_resumida)
    df_porc_p15 = analise.grafico_pie_p15(df_exp_vinho_litros_resumida1)
    #st.dataframe(df_porc_p15)
    fig = go.Figure()
    fig.add_pie(labels=df_porc_p15['grupo'], values=df_porc_p15['total_dolares'])
    st.plotly_chart(fig)
    #st.pyplot(plt.pie(df_porc_p15['total_dolares'], labels=df_porc_p15['grupo']))
    #plt.show()

with st.expander('Total de importação em dólar por continente'):
    s_p15_regiao = analise.grafico_bar_p15_by_regiao(df_exp_vinho_litros_resumida1)
    fig = go.Figure(data=[
        go.Bar(name="Total em US$", x=s_p15_regiao.index, y=s_p15_regiao, marker_color='indianred'),
    ])
    
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=1300, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    
    st.plotly_chart(fig)
    #st.dataframe(s_p15_regiao)

with st.expander('Tendencia de exportação de cada continente'):
    df_exp_vinho_maiores_lucros = df_exp_vinho_litros.sort_values(by='Total em US$', ascending=False)
    cols = df_exp_vinho_maiores_lucros.columns[1::2][-16:]
    df_exp_vinho_maiores_lucros = df_exp_vinho_maiores_lucros[cols]

    df_p15 = analise.grafico_line_p15_by_regiao(df_exp_vinho_maiores_lucros)
    fig = go.Figure()
    exec = 0
    for list in df_p15.values.tolist():
        fig.add_trace(go.Scatter(x=df_p15.columns, y=list, name=df_p15.index[exec]))
        exec +=1    
    
    fig.update_layout(autosize=False, width=1300, height=500)
    st.plotly_chart(fig)
    #st.dataframe(df_p15)

with st.expander('Total de exportação por nível socioeconomico'):
    df_p15 = analise.grafico_bar_p15_by_socio(df_exp_vinho_maiores_lucros)
    # y = total em dolar
    # x = df.index
    fig = go.Figure(data=[
        #go.Bar(name="Total em US$", x=df_exp_vinho_litros.columns[0::2][:-1], y=v0, marker_color='indianred'),
        go.Bar(name="Total paises", x=df_p15.index, y=df_p15['Total em US$'], marker_color=['lightsalmon','indianred', 'lightsalmon'])
    ])
    
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=1300, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    
    st.plotly_chart(fig)
    #st.dataframe(df_p15)

with st.expander('Tendencia de exportação em dólar por nivel socioeconomico'):
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

with st.expander('Quantidade de paises por nivel socioeconomico'):
    df_p15 = analise.grafico_bar_p15_qtde_by_socio(df_exp_vinho_maiores_lucros)

    fig = go.Figure(data=[
        #go.Bar(name="Total em US$", x=df_exp_vinho_litros.columns[0::2][:-1], y=v0, marker_color='indianred'),
        go.Bar(name="Total paises", x=df_p15.index, y=df_p15, marker_color=['lightsalmon','indianred', 'lightsalmon'])
    ])
    
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=1300, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    
    st.plotly_chart(fig)
    #st.dataframe(df_p15)

with st.expander('Comparação dos paises que mais consomem com a o GPD'):
    df_p15 = analise.df_gdp(df_exp_vinho_maiores_lucros)
    st.dataframe(df_p15)