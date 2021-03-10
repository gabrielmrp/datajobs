
import xlsxwriter

import streamlit as st
import numpy as np
import pandas as pd
import core as core
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from pylab import rcParams
from io import BytesIO


def get_table_download_link(df,filename,description,ftype):
    """Generates a link allowing the data in a given panda dataframe to be downloaded 
    """
    def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer,index=False)
            writer.save()
            processed_data = output.getvalue()
            return processed_data


    if(ftype=='csv'):
        df = df[["company","text","url","charge"]]

        xlsx = to_excel(df)
        b64 = base64.b64encode(xlsx).decode()  # some strings <-> bytes conversions necessary here
        href= f'<a href="data::application/octet-stream;base64,{b64}" download="'+filename+'">'+description+'</a>'
    else:
        b64 = base64.b64encode(open(filename,"r",encoding="utf-8").read().encode()).decode()  
        href = f'<a href="data:file/txt;base64,{b64}" download="'+filename+'">'+description+'</a>'
    return href



def create_barplot(data_items):
    fig = plt.gcf() 
    bp = sns.barplot(x="Contagem",
                             y="Item",
                             hue=None,
                              palette="Set2",
                             data=data_items)
    fig.set_size_inches(12, 6)  
    sns.color_palette("mako" )
    return bp
   




def put_text_barplot(bp,spacement): 
    for p in bp.patches:
        width = p.get_width()      
        bp.text(width + spacement,       
                        p.get_y() + p.get_height() / 2, 
                        '{:1.0f}'.format(width), 
                        ha = 'left',    
                        va = 'center')   
    
    
     
def main(): 
    
    
    
    #check if in development to hide menu
    try:
        open("indev.txt","r")
        hide_streamlit_menu = """#MainMenu {visibility: hidden;}footer {visibility: hidden;}"""
    except:
        hide_streamlit_menu=""
        

    #get the data
    df,db_df,df_src = core.operation()
    charge_dict = {'Analista de BI':'BI',
                   'Cientista de Dados':'CD',
                   'Eng. de Dados':'BD'
                    }
    
    #interface setup
        
    st.set_page_config(page_title='Datajobs', page_icon = 'favicon.ico', layout = 'wide', initial_sidebar_state = 'auto')
    c1, c2, c3, c4 = st.beta_columns((1, 6, 1 , 1)) 
    f = open("static/styles.css", "r") 
    st.markdown("<style>"+f.read()+hide_streamlit_menu+"</style>", unsafe_allow_html=True)


    #Description  
    c2.markdown("""<div class='banner'></div> """, unsafe_allow_html=True) 
    c2.header('Objetivo')
    c2.write('O objetivo principal proporcionar uma visão sobre cargos e ferramentas utilizadas na área de dados, proporcionando:')   
    c2.markdown("""
                <ol>
                <li>Tecer comparativos entre os principais cargos da área quanto ao tipo de ferramentas que utilizam, para assim ajudar a escolher qual cargo focar a partir de seu background e/ou uso de ferramentas de interesse;</li>
                <li>Verificar quais são ferramentas mais utilizadas nas áreas  por categoria, para o caso de querer escolher um curso ainda não tendo definido o cargo de interesse;</li>
                <li>Verificar quais ferramentas são mais utilizadas no cargo de interesse, isso caso queira escolher um curso e já tenha definido o cargo de interesse.</li> 
                </ol>
                """, unsafe_allow_html=True)        
    c2.header('Metodologia')  
    c2.markdown("""
                <b>Coleta</b>
                """, unsafe_allow_html=True)   
    c2.write('Procedimento: Coleta manual de informações de vagas em sites de vagas seguindo os critérios:')
    c2.markdown("""
                <ul>
                <li>Cargos: Analista de BI, Cientista de Dados, Eng. de Dados;</li>
                <li>Fontes: Google Vagas e Linkedin;</li>
                <li>Cidade: Belo Horizonte - MG;</li>
                <li>Período: Março/2020.</li>
                </ul>
                """, unsafe_allow_html=True)

    c2.write('Tabulação: Inserção em planilha "Excel" contendo como colunas: "company" (empresa) ,"text" (descritivo) e "url" (endereço) e "charge" (cargo)')

    c2.markdown(get_table_download_link(df_src,'source.xlsx','Baixar Fonte de Dados','csv'), unsafe_allow_html=True)        
    c2.write('As stacks foram coletadas manualmete a partir de sites de recrutamento, como: Programathor, Revelo e Geekhunter')
 

    c2.markdown(get_table_download_link(df_src,'stacklist.json','Baixar lista de Stacks','json'), unsafe_allow_html=True)
    c2.markdown("""
                <b>Processamento</b>
                """, unsafe_allow_html=True)  
    c2.write('Categorização: A partir da exploração dos dados foi possível categorizar os stacks de acordo com diferentes categorias:')
    c2.markdown("""<ul>
                <li>Banco de Dados;</li>
                <li>Software/Visualização;</li>
                <li>Linguagem de Programação;</li>
                <li>Serviços;</li>
                <li>Bibliotecas e Frameworks.</li>
                </ul>
        """, unsafe_allow_html=True)
    c2.write('Construiu-se então um dicionário de correspondência, para tal utilizou-se basicamente o site wikipedia.org')

    c2.markdown(get_table_download_link(df_src,'categories.json','Baixar Categorização','json'), unsafe_allow_html=True)

    c2.write('Com os dados categorizados, realizaram-se as análises expostas no menu "Apresentação"')
  
    c2.markdown("""
                <b>Resultados</b>
                """, unsafe_allow_html=True) 


    c2.header('Comparação de Cargos na Área de Dados')
    c2.write('O Eixo "Contagem de itens" se refere ao número de itens em vagas encontrados, excluíndo-se duplicações em uma mesma vaga')

    ##########################################################################
    #dataframe operations
    df.columns=['Analista de BI', 'Cientista de Dados', 'Eng. de Dados']
    df2 = pd.DataFrame(df.unstack()).reset_index()
    df2.columns=['Cargo','Categoria','Contagem de itens']
    
    
    #plot operations
    plt.figure(figsize=(9, 4))
    fig = plt.gcf()
    sns.color_palette("mako"  )
    sb = sns.barplot(x="Categoria", y="Contagem de itens",palette="Set2", hue="Cargo", data=df2)
    sb.set_xticklabels(sb.get_xticklabels(), 
                          rotation=45, 
                          horizontalalignment='right')
    c2.pyplot(fig)
    plt.close()
    sb.set_xticklabels('')

     ##########################################################################
    
    c2.header('Stacks por Categoria') 
    c2.write('Nessa análise trabalhamos com o montante de vagas, será indicada a quantidade de vagas em que um determinado "Item" é citado.')  
    
    categories = db_df.category.unique().tolist()
    
    for cat in categories:
         if(cat!='Outros'):
             
              
            c2.markdown("<b class='category'>"+cat+"</b>", unsafe_allow_html=True)
            
            #dataframe operations
            item_category = db_df[db_df.category==cat].groupby(['item','category']).sum().sort_values(['count'],ascending=False).head(5).reset_index()[['item','count']].set_index(['item'])
            item_category.reset_index(inplace=True)
            item_category.rename(columns={'item':'Item','count':'Contagem'},inplace=True)
 
            #plot operations    
            fig = plt.gcf()            
            bp1 = create_barplot(item_category)             
            put_text_barplot(bp1,spacement=1)
            c2.pyplot(fig)
            bp1.clear() 
 
             
    ##########################################################################
    c2.header('Stacks por Cargo e Categoria')
    c2.write('Nessa análise podem ser escolhidos as "Categorias" e "Cargos" através dos menus de seleção abaixo, será indicada a quantidade de vagas em que um determinado "Item" é citado.')  

    #dataframe operations
    charge = c2.selectbox("Escolha um cargo:", ['Analista de BI', 'Cientista de Dados', 'Eng. de Dados']) 
    category = c2.selectbox("Escolha uma categoria:", df.index.tolist()) 
    items = db_df[(db_df.charge==charge_dict[charge])&(db_df.category== category )]
    items = items[['item','count']]
    items.rename(columns={'item':'Item','count':'Contagem'},inplace=True)        
    
    
    #plot operations
    bp2 = create_barplot(items) 
    put_text_barplot(bp2,spacement=0.1)    
    c2.pyplot(fig)        
 
    #generate csv
    df_src.rename(columns={'company':'Empresa','text':'Descrição','url':'url','charge':'Cargo'},inplace=True)
    c2.write('O código completo está publicado no endereço abaixo, dúvidas e sugestões são muito bem-vindas')

    #profile
    pf = open("static/perfil.html", "r")
    c2.markdown(pf.read(),unsafe_allow_html=True)
 
if __name__ == '__main__':
    main()
    
    
    
     
