

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 22:31:31 2020

@author: gabri
"""
from collections import Counter
import json
import re
import streamlit as st
import pandas as pd 

def operation():    

    charge_stack_count={}
    dataframe_final = []
 
    #translate terms 
    def corresp(val,file):
        
        with open(file+'.json', encoding='utf-8') as json_file:
            dict_words = json.load(json_file) 
         
        if(val in dict_words):
            return dict_words[val]
        else:
            return val
    
    
    #capture used terms in files
    df_src = pd.DataFrame()
    src = pd.read_excel('source.xlsx',engine='openpyxl') 
    src = src[['company', 'text', 'url', 'charge']]
    
    for charge in ["BI","CD","ED"]: 
        
        #get data        
        data = json.loads(src[src.charge==charge].to_json(orient="records",force_ascii=False))
        
         #remove not literal chars
        texts = [re.sub("[/,\():;.]","",d["text"]) for d in data]
        
        #get all stacks
        with open("stacklist.json", encoding='utf-8') as stacklist:
            stack = json.load(stacklist)
         
        
        #count all stacks with repetition
        count_all_stacks = [] 
        for t1 in texts:
            for a in stack:   
                if( " "+a.lower()+" " in t1.lower()):count_all_stacks.append(corresp(a,'terms'))
            
        #count stacks by entry     
        count_stack_by_entry = []             
        for i in Counter(count_all_stacks).most_common():
            if(i[1]>2):
                count_stack_by_entry.append(i)
                dataframe_final.append([charge,corresp(i[0],'terms'),corresp(i[0],'categories'),i[1]])
        
        #put in the dataframe 
        charge_stack_count[charge] = count_stack_by_entry
        
        dataframe_aux = pd.DataFrame(data)        
        dataframe_aux["charge"]=charge
        
        df_src = pd.concat([df_src,dataframe_aux])
        
        
    #create a dict of charge and counts 
    charge_dict={};
    
    for charge in charge_stack_count.keys():
        charge_dict[charge]={}
        for item in charge_stack_count[charge]:
            category = corresp(item[0],'categories') 
            charge_dict[charge][category] = (charge_dict[charge][category]+item[1] if category in charge_dict[charge] else 0)
    
    #put the dict in the dataframe   
    df = pd.DataFrame()
    df = df.from_dict(charge_dict)    
    df.drop(['Outros'],inplace=True)
    
    db_df = pd.DataFrame(dataframe_final,columns=['charge','item','category','count'])
    return df,db_df,df_src

    
