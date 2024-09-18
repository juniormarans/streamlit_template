import streamlit as st
from services import ApiClient

def display():
    with st.form(key='user_form'):
        name = st.text_input('Nome')
        email = st.text_input('Email')
        role = st.selectbox('Papel', ['Admin', 'Editor', 'Viewer'])
        submit_button = st.form_submit_button(label='Adicionar Usuário')

    if submit_button:
        user_data = {'name': name, 'email': email, 'role': role}
        ApiClient.create_user(user_data)
        st.success('Usuário adicionado com sucesso!')
