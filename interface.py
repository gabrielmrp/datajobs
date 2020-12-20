

import streamlit as st
import numpy as np
import pandas as pd
import core as core
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import streamlit.components.v1 as components
from pylab import rcParams

def get_table_download_link(df,filename,description):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="'+filename+'">'+description+'</a>'
    return href


    
def main():
    
    charge_dict = {'Analista de BI':'BI',
                   'Cientista de Dados':'CD',
                   'Eng. de Dados':'BD'
                    }
    df,db_df,df_src = core.operation()
    
    st.set_page_config(page_title='Datajobs', page_icon = 'favicon.ico', layout = 'wide', initial_sidebar_state = 'auto')
    st.markdown("""
                <style>
                .big-font {
                    font-size:10px !important;
                }
                .stDataFrame{margin:0 50%}
                </style>
                """, unsafe_allow_html=True)


    selection = st.sidebar.radio("Menu", ['Apresentação','Metodologia'])


    if(selection=='Metodologia'):
     
    #if st.sidebar.button('Metodologia'):         
        st.write('Procedimento: Coleta manual de informações de vagas em sites de vagas')
        st.markdown("""
                    <ul>
                    <li>Cargos: Analista de BI, Cientista de Dados, Eng. de Dados</li>
                    <li>Fontes: Google Vagas e Linkedin</li>
                    <li>Belo Horizonte - MG </li>
                    <li>Março/2020</li>
                    </ul>
                    """, unsafe_allow_html=True)

        st.write('Inserção em planilha "Excel" contendo como colunas: "company","text" e "url", gerando os arquivos para cada cargo')

        st.markdown(get_table_download_link(df_src,'source.xlsx','Fonte de Dados'), unsafe_allow_html=True)        
        st.write('As stacks foram coletadas a partir de sites de recrutamento, como Programathor, Revelo e Geekhunter')

        st.markdown(get_table_download_link(df_src,'stacks.json','Baixar lista de Stacks'), unsafe_allow_html=True)

        st.write('A partir da exploração dos dados foi possível categorizar os stacks de acordo com diferentes categorias e, assim, construir um dicionário de correspondência, para tal utilizou-se basicamente o site wikipedia.org')
        st.markdown(get_table_download_link(df_src,'categories.json','Baixar Categorização'), unsafe_allow_html=True)
        st.write('O código completo está publicado no endereço abaixo, dúvidas e sugestões são bem-vindas')

        st.markdown("""<a href='https://github.com/gabrielmrp/datajobs' target='_blank'>Link para o Github</a>""", unsafe_allow_html=True)
        
         
    else:
        st.header('Comparação de Cargos na Área de Dados')
        df.columns=['Analista de BI', 'Cientista de Dados', 'Eng. de Dados']
        df2 = pd.DataFrame(df.unstack()).reset_index()
        df2.columns=['Cargo','Categoria','Contagem']
        plt.figure(figsize=(16, 6))
        fig = plt.gcf()
        sb = sns.barplot(x="Categoria", y="Contagem", hue="Cargo", data=df2)
        sb.set_xticklabels(sb.get_xticklabels(), 
                              rotation=45, 
                              horizontalalignment='right')
        st.pyplot(fig)
        st.write('O Eixo "Contagem" se refere ao número de termos encontrados, excluíndo-se duplicações em uma mesma vaga')

        rcParams['figure.figsize'] = 5, 8



        st.header('Stacks por Cargo e Categoria')    
        charge = st.selectbox("Escolha um cargo:", ['Analista de BI', 'Cientista de Dados', 'Eng. de Dados'])
        
        category = st.selectbox("Escolha uma categoria:", df.index.tolist())
        
        
        items = db_df[(db_df.charge==charge_dict[charge])&(db_df.category== category )]
        items = items[['item','count']]
        items.rename(columns={'item':'Item','count':'Contagem'},inplace=True)        
        st.dataframe(items.set_index(['Item']),width=1024, height=768)



        
        st.header('Stacks por Categoria (Todos os Cargos)') 
        
        categories = db_df.category.unique().tolist()
        
        for cat in categories:
             if(cat!='Outros'):
                st.write(cat)
                #st.markdown('<i class="big-font">Hello World !!</i>', unsafe_allow_html=True)
                item_categoria = db_df[db_df.category==cat].groupby(['item','category']).sum().sort_values(['count'],ascending=False).head(5).reset_index()[['item','count']].set_index(['item'])
                item_categoria.rename(columns={'item':'Item','count':'Contagem'},inplace=True)
                st.dataframe(item_categoria)
                
                
        
        df_src.rename(columns={'company':'Empresa','text':'Descrição','url':'url','charge':'Cargo'},inplace=True)
        
 
if __name__ == '__main__':
    main()
    
    
    
     