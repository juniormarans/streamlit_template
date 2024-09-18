import streamlit as st
from components import RoleTable, RoleForm

def show():
    st.title("Gerenciamento de Papéis")

    st.subheader("Lista de Papéis")
    RoleTable.display()

    st.subheader("Adicionar Novo Papel")
    RoleForm.display()
if __name__ == "__main__":
    show()