import streamlit         as st
import pandas            as pd
import numpy             as np
import seaborn           as sns
import matplotlib.pyplot as plt
import altair            as alt
from st_aggrid        import AgGrid, GridOptionsBuilder

PRIMARY_COLOR = "#572b52"

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
colunas = colunas.insert(0, df_exp_vinho.columns[0])

new_columns_name = []
for col in df_exp_vinho.columns:
    if str(col) == 'País':
        new_columns_name.append(col)
        
    if str(col).endswith(".1"):
        new_columns_name.append(str(col).replace(".1", " US$"))
        
    elif not str(col).endswith(".1") and not str(col) == "País":
        new_columns_name.append(str(col).replace(".1", " US$"))

df_exp_vinho = df_exp_vinho[colunas]

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
    
    st.subheader("Tabela Resumida com Informações de Exportações nos Últimos Anos")
    df_exp_vinho_litros_resumida1 = df_exp_vinho_litros_resumida.reset_index()
    builder = GridOptionsBuilder.from_dataframe(df_exp_vinho_litros_resumida1)
    builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=7)
    go                        = builder.build()
    AgGrid(df_exp_vinho_litros_resumida1, gridOptions=go)

    #graph = alt.Chart(df_exp_vinho).mark_boxplot().encode(y="Total em Litros").properties(width=500)
    
    df_sample = df_exp_vinho_litros_resumida.loc[(df_exp_vinho_litros_resumida["Total em Litros"] > 100000) & (df_exp_vinho_litros_resumida["Total em Litros"] <= 1000000)].sort_values(by="Total em Litros", ascending=False)
    plt.figure(figsize=(22,8))
    x_axis = np.arange(len(df_sample.index))
    plt.bar(x_axis - 0.2, df_sample[['Total em Litros']].T.sum().values,width=0.4, label = "Litros")
    plt.bar(x_axis + 0.2, df_sample[['Total em US$']].T.sum().values,width=0.4,  label="Valor US$")
    plt.ticklabel_format(style='plain', axis='y')
    plt.xticks(x_axis, df_sample.index)
    plt.xticks(rotation=90)
    #plt.axhline(y=df_exportacao_geral_litros.sum().median(), color='red', linestyle='--', linewidth=3, label='Mediana')
    #plt.axhline(y=df_exportacao_geral_litros.sum().mean(), color='blue', linestyle='--', linewidth=3, label='Média')
    plt.title("Linha do Tempo de Exportação de Vinho e Lucro(US$) do Brasil nos Últimos 15 anos")
    plt.legend();
    
    
