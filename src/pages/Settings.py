import streamlit as st
from components import Charts

__all__ = ["show"]

def show():
    st.title("Página Seetings")
    st.write("Bem-vindo à Página Inicial!")
    # Exemplo de uso de componente
    data = {'Date': ['2021-01-01', '2021-01-02'], 'Value': [10, 20]}
    Charts.render_chart(data)

if __name__ == "__main__":
    show()