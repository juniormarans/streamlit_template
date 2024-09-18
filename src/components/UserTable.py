import streamlit as st
from pydantic import ValidationError
import pandas as pd
from services import ApiClient
import models, schema
from schema import GetUser

def display():
    # Obter dados da API
    query = models.User.query_params(all_data=True, operator="=", skip=0,limit=100)
    users = [GetUser.model_validate(data).model_dump() for data in query.data]
    df = pd.DataFrame(users)
    # Exibir tabela
    st.dataframe(df)
