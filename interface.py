

import streamlit as st
import numpy as np
import pandas as pd
import core as core
import seaborn as sns
import matplotlib.pyplot as plt
import base64

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="dados.csv">Baixar fonte de dados</a>'
    return href
    
def main():
    
    charge_dict = {'Analista de BI':'BI',
                   'Cientista de Dados':'CD',
                   'Eng. de Dados':'BD'
                    }
    
    st.header('Comparação de Cargos na Área de Dados')
    #st.write('Esta é uma página de teste.')
    df,db_df,df_src = core.operation()
    df.columns=['Analista de BI', 'Cientista de Dados', 'Eng. de Dados']
    df2 = pd.DataFrame(df.unstack()).reset_index()
    df2.columns=['Cargo','Categoria','Contagem']
    sb = sns.barplot(x="Categoria", y="Contagem", hue="Cargo", data=df2)
    sb.set_xticklabels(sb.get_xticklabels(), 
                          rotation=45, 
                          horizontalalignment='right')
    st.pyplot()
    st.header('Stacks por Cargo e Categoria')

    charge = st.selectbox("Escolha um cargo:", ['Analista de BI', 'Cientista de Dados', 'Eng. de Dados'])
    
    category = st.selectbox("Escolha uma categoria:", df.index.tolist())
    
    
    items = db_df[(db_df.charge==charge_dict[charge])&(db_df.category== category )]
    items = items[['item','count']]
    items.rename(columns={'item':'Item','count':'Conta'},inplace=True)
    
    st.dataframe(items.set_index(['Item']),width=1024, height=768)
    
     
    
    df_src.rename(columns={'company':'Empresa','text':'Descrição','url':'url','charge':'Cargo'},inplace=True)
    st.markdown(get_table_download_link(df_src), unsafe_allow_html=True)
    
if __name__ == '__main__':
    main()
    
    
    
     