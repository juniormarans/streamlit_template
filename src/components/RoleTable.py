import streamlit as st
import pandas as pd
from services import ApiClient

def display():
    # Obter dados da API
    roles = ApiClient.get_roles()
    df = pd.DataFrame(roles["data"])
    # Exibir tabela
    st.dataframe(df)
