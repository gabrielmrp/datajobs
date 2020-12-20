

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 22:31:31 2020

@author: gabri
"""
from collections import Counter
import json
import re
import streamlit as st


def operation():    

    c={}
    db = []
 
    #translate terms 
    def corresp(val,file):
        
        with open(file+'.json', encoding='utf-8') as json_file:
            dict_words = json.load(json_file) 
         
        if(val in dict_words):
            return dict_words[val]
        else:
            return val
    
    import pandas as pd 
    #capture used terms in files
    df_src = pd.DataFrame()
    src = pd.read_excel('source.xlsx',engine='openpyxl')
    
    for charge in ["BI","CD","ED"]:
        filename = charge+".json"
        print(charge)
        dx = pd.DataFrame()
        
        #with open(filename, encoding='utf-8') as json_file:
          #   data = json.load(json_file)
        
        data = json.loads(src[src.charge==charge].to_json(orient="records",force_ascii=False))
        
        with open("stacklist.json", encoding='utf-8') as stacklist:
            stack = json.load(stacklist)
        
        
        texts = [re.sub("[/,\():;.]","",d["text"]) for d in data]
        
        counts = [] 
        for t1 in texts:
            for a in stack:   
                if( " "+a.lower()+" " in t1.lower()):counts.append(corresp(a,'terms'))
                 
        count = []             
        for i in Counter(counts).most_common():
            if(i[1]>2):
                count.append(i)
                db.append([charge,corresp(i[0],'terms'),corresp(i[0],'categories'),i[1]])
        
        
        c[charge] = count
        
        dx = pd.DataFrame(data)
        
        dx["charge"]=charge
        df_src = pd.concat([df_src,dx])
        
        
    with open('categories.json', encoding='utf-8') as json_file:
            categories = json.load(json_file)    
        
    d={};
    
    for charge in c.keys():
        d[charge]={}
        for item in c[charge]:
            category = corresp(item[0],'categories') 
            d[charge][category] = (d[charge][category]+item[1] if category in d[charge] else 0)
     
             
    
    df = pd.DataFrame()
    df = df.from_dict(d)
    
    df.drop(['Outros'],inplace=True)
    
    db_df = pd.DataFrame(db,columns=['charge','item','category','count'])
    return df,db_df,df_src

#exploratory analisis


def watch_not_selected():
    res=[]    
    for charge in ["BI","CD","ED"]:
        filename = charge+".json"    
        sum([ re.split(" ",t) for t in texts],[])
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
        texts = [re.sub("[/,\():;.]","",d["text"]) for d in data]
        res.append(sum([ re.split(" ",t) for t in texts],[]))
    
    all_words = [(x[0].lower(),x[1]) for x in Counter(sum(res,[])).most_common()    ]
    stack_terms = [x.lower() for x in stack]
    
    
    
    return [i for i in all_words if i[0] not in stack_terms]
    
    
