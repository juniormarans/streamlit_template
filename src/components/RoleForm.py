import streamlit as st
from services import ApiClient

def display():
    with st.form(key='role_form'):
        role_name = st.text_input('Nome do Papel')
        permissions = st.multiselect('Permissões', ['Ler', 'Escrever', 'Atualizar', 'Excluir'])
        submit_button = st.form_submit_button(label='Adicionar Papel')

    if submit_button:
        role_data = {'name': role_name, 'permissions': permissions}
        ApiClient.create_role(role_data)
        st.success('Papel adicionado com sucesso!')
