import streamlit as st
from pages import UserManagement, RoleManagement



def main():
   
    st.set_page_config(page_icon=":material/add_circle:", page_title="Painel de Administração", layout="wide")

    st.title("Página Inicial")
    st.write("Bem-vindo ao Painel de Administração!")

if __name__ == "__main__":
    main()
