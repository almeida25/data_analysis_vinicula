import streamlit         as st
import pandas            as pd
import numpy             as np
import seaborn           as sns
import matplotlib.pyplot as plt
import altair            as alt
import plotly.express    as px
import plotly.graph_objs as go
from st_aggrid        import AgGrid, GridOptionsBuilder

PRIMARY_COLOR = "#572b52"

def main():
    st.header("Projeto da Vitivinicultura")
    st.write(" Apresentamos um projeto de análise da importação e exportação da Vitivinicultura como uma oportunidade estratégica de investimento. A indústria vinícola, com seu potencial de crescimento e lucratividade, tem se mostrado cada vez mais atrativa para investidores interessados em explorar os mercados internacionais de vinho.")
    st.write("Uma das principais vantagens competitivas desta vinícola é a sua capacidade de combinar tradição e inovação. Com uma equipe de enólogos experientes, que valorizam as técnicas tradicionais de vinificação, mas também estão abertos à adoção de métodos inovadores, a vinícola tem conseguido criar vinhos que encantam paladares exigentes em todo o mundo. Além disso, a vinícola tem uma sólida estratégia de comércio e produção para sustentar suas atividades de importação e exportação. A produção é cuidadosamente planejada, levando em consideração as demandas e tendências do mercado global de vinhos.")
    st.write("No que se refere ao comércio, a empresa busca estabelecer parcerias estratégicas com distribuidores e importadores em mercados-chave ao redor do mundo. Essas parcerias permitem a ampla distribuição dos vinhos da vinícola em diferentes regiões, atingindo consumidores exigentes e explorando novas oportunidades de negócio.")


    st.header("Objetivo do Projeto")
    st.write("O objetivo é demonstrar análises abrangentes da importação e exportação da Vitivinicultura, com foco em fornecer informações relevantes para investidores interessados em explorar as oportunidades de negócios nesse setor. Buscamos identificar as principais tendências, desafios e oportunidades do comércio internacional de vinhos, analisando as dinâmicas globais do mercado e distribuição.")
    st.write("Neste contexto, o presente projeto tem como objetivo analisar também detalhadamente o comércio e a produção da vinícola no âmbito da importação e exportação de vinhos. Ao realizar essa análise aprofundada da importação e exportação de vinhos do Brasil, esperamos contribuir para o entendimento e a valorização dessa indústria, bem como fornecer insights para aqueles que desejam se envolver nesse mercado em expansão, também espera-se oferecer aos investidores uma visão clara e abrangente sobre a vinícola, destacando as vantagens competitivas, o potencial de crescimento e as oportunidades de investimento no setor. Essas informações serão fundamentais para embasar decisões estratégicas e maximizar o retorno sobre o investimento.")


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
    df_exp_vinho_litros_resumida1 = df_exp_vinho_litros_resumida.reset_index()
    builder = GridOptionsBuilder.from_dataframe(df_exp_vinho_litros_resumida1)
    builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=7)
    gol                        = builder.build()
    AgGrid(df_exp_vinho_litros_resumida1, gridOptions=gol)

    
with st.expander(" Maiores Exportadores de Vinho"):
    #px.line()
    st.subheader("Linha do Tempo dos Países que mais geraram Lucro ao Brasil nos Últimos 15 Anos")
    df_exp_vinho_maiores_lucros = df_exp_vinho_litros.sort_values(by='Total em US$', ascending=False)
    cols = df_exp_vinho_maiores_lucros.columns[1::2]
    df_exp_vinho_maiores_lucros = df_exp_vinho_maiores_lucros[cols]
    #st.write(df_exp_vinho_maiores_lucros)
    df_sample = df_exp_vinho_maiores_lucros.head(10)
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
    v0 = df_exp_vinho_litros[df_exp_vinho_litros.columns[1::2][:-1]].sum().values.tolist()
    v1 = df_exp_vinho_litros[df_exp_vinho_litros.columns[0::2][:-1]].sum().values.tolist()

    fig = go.Figure(data=[
        go.Bar(name="Total em Litros(Kg)", x=df_exp_vinho_litros.columns[0::2][:-1], y=v0, marker_color='indianred'),
        go.Bar(name="Total em US$", x=df_exp_vinho_litros.columns[0::2][:-1], y=v1, marker_color='lightsalmon')
    ])
    
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(autosize=False, width=1300, height=500, xaxis_tickangle=0, xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   ))
    st.plotly_chart(fig)
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
