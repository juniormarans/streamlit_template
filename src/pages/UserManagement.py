import streamlit as st
from components import UserTable, UserForm

def show():
    st.title("Gerenciamento de Usuários")

    st.subheader("Lista de Usuários")
    UserTable.display()

    st.subheader("Adicionar Novo Usuário")
    UserForm.display()
if __name__ == "__main__":
    show()