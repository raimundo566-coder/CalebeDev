# ARQUIVO: app.py
# ATUALIZAÇÃO: Com Filtro de Categorias

import streamlit as st
import pandas as pd
from dominios import PontoTuristico

# 1. Configuração
st.set_page_config(page_title="Guia Chapada", page_icon="🌵", layout="wide")

# 2. Dados
@st.cache_data
def carregar_dados():
    return [
        PontoTuristico("Complexo Pedra Caída", "Aventura", (-7.0448, -47.4412), 
                       "Santuário com tirolesa.", "Sanctuary with zipline.", False),
        PontoTuristico("Poço Secreto", "Relax", (-7.3200, -47.4500), 
                       "Água azul turquesa.", "Turquoise water.", True),
        PontoTuristico("Portal da Chapada", "Trilha", (-7.0300, -47.4300), 
                       "Vista do morro.", "View from the hill.", False)
    ]

catalogo = carregar_dados()

# 3. Barra Lateral (Menu e FILTROS)
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Navegação", ["🏠 Início", "📊 Relatório", "🗺️ Mapa"])
st.sidebar.markdown("---")

# --- NOVIDADE: O FILTRO ---
st.sidebar.header("Filtros")
categoria_selecionada = st.sidebar.selectbox(
    "Escolha a Categoria:",
    ["Todas", "Aventura", "Relax", "Trilha"]
)
# ---------------------------

# 4. Telas
if opcao == "🏠 Início":
    st.title("🌵 Guia Chapada das Mesas")
    st.info("Bem-vindo! Use o menu ao lado para explorar.")
    col1, col2 = st.columns(2)
    col1.metric("Locais Totais", len(catalogo))
    col2.metric("Status do Sistema", "Online")

elif opcao == "📊 Relatório":
    st.header("Relatório Gerencial")
    
    # APLICANDO O FILTRO
    lista_filtrada = []
    if categoria_selecionada == "Todas":
        lista_filtrada = catalogo
    else:
        # Só adiciona se a categoria for igual à selecionada
        for item in catalogo:
            if item.tipo == categoria_selecionada:
                lista_filtrada.append(item)
    
    # Exibe a tabela (agora filtrada)
    if not lista_filtrada:
        st.warning("Nenhum local encontrado nesta categoria.")
    else:
        dados = [{"Nome": i.nome, "Tipo": i.tipo, "Desc": i.desc_pt} for i in lista_filtrada]
        st.dataframe(pd.DataFrame(dados), use_container_width=True)

elif opcao == "🗺️ Mapa":
    st.header("Mapa de Localização")
    # Mapa também pode obedecer ao filtro se você quiser
    dados_mapa = [{"lat": i.gps[0], "lon": i.gps[1], "nome": i.nome} for i in catalogo]
    st.map(pd.DataFrame(dados_mapa))
