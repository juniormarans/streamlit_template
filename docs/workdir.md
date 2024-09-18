# index

```bash
frontend/
├── src/                      # Código fonte do frontend
    ├── app.py                    # Ponto de entrada da aplicação Streamlit
    ├── requirements.txt          # Dependências do frontend (Streamlit, pandas, etc.)
    ├── README.md                 # Documentação do frontend
    ├── pages/                    # Páginas modulares do aplicativo
    │   ├── __init__.py
    │   ├── page1.py              # Página 1 (subaplicação ou parte da interface)
    │   ├── page2.py              # Página 2
    │   └── page3.py              # Página 3
    ├── components/               # Componentes reutilizáveis (gráficos, tabelas, etc.)
    │   ├── __init__.py
    │   ├── charts.py             # Funções para criação de gráficos (Streamlit + Plotly, Matplotlib, etc.)
    │   ├── tables.py             # Funções para criação de tabelas (Streamlit + pandas)
    │   └── forms.py              # Funções para criação de formulários
    ├── services/                 # Lógica de negócios e comunicação com a API
    │   ├── __init__.py
    │   ├── api_client.py         # Funções para se comunicar com o backend (FastAPI)
    │   └── data_processing.py    # Funções para carregar e processar dados
    ├── assets/                   # Arquivos estáticos (CSS, imagens, etc.)
    │   ├── styles.css            # Arquivo de estilos customizados
    │   └── images/               # Diretório de imagens (ex: logo, ícones)
    │       └── logo.png
    └── tests/                    # Testes do frontend
        ├── test_charts.py        # Testes de visualização (ex: gráficos)
        ├── test_forms.py         # Testes de formulários
        └── test_pages.py         # Testes das páginas
```