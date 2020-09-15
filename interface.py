

import streamlit as st
import numpy as np
import pandas as pd
def main():
    page = st.sidebar.selectbox("Escolha uma opção:", ['Opção 1', 'Opção 2', 'Opção 3'])
    st.header('Tutorial Streamlit - Heroku')
    st.write('Esta é uma página de teste.')
if __name__ == '__main__':
    main()