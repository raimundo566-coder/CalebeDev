# ARQUIVO: app.py
# OBJETIVO: Web App Comercial com Streamlit

import streamlit as st
import pandas as pd
from dominios import PontoTuristico

# 1. Configuração da Página (Título da Aba do Navegador)
st.set_page_config(
    page_title="Guia Chapada das Mesas",
    page_icon="🌵",
    layout="wide"  # Usa a tela inteira
)


# 2. O Banco de Dados (Igual ao anterior)
@st.cache_data  # Um truque para não recarregar os dados toda hora
def carregar_dados():
    p1 = PontoTuristico("Complexo Pedra Caída", "Aventura", (-7.0448, -47.4412),
                        "Santuário com tirolesa.", "Sanctuary with zipline.", False)
    p2 = PontoTuristico("Poço Secreto", "Relax", (-7.3200, -47.4500),
                        "Água azul turquesa.", "Turquoise water.", True)
    p3 = PontoTuristico("Portal da Chapada", "Trilha", (-7.0300, -47.4300),
                        "Vista do morro.", "View from the hill.", False)
    return [p1, p2, p3]


catalogo = carregar_dados()

# 3. A Barra Lateral (Menu)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=100)
st.sidebar.title("Menu Principal")
opcao = st.sidebar.radio("Escolha uma visão:", ["🏠 Início", "📊 Relatório Gerencial", "🗺️ Mapa via Satélite"])

# 4. Construção das Telas
st.title("🌵 Guia Oficial: Chapada das Mesas")
st.markdown("---")  # Uma linha divisória bonita

if opcao == "🏠 Início":
    st.write("Bem-vindo ao sistema de gestão turística.")
    st.info("Selecione uma opção no menu lateral para começar.")

    # Exemplo de cartão visual (Métrica)
    col1, col2 = st.columns(2)
    col1.metric("Locais Cadastrados", len(catalogo))
    col2.metric("Temperatura Média", "32°C")

elif opcao == "📊 Relatório Gerencial":
    st.subheader("Tabela de Dados")

    # Preparando os dados para a Web
    dados_dict = []
    for item in catalogo:
        dados_dict.append({
            "Nome": item.nome,
            "Categoria": item.tipo,
            "Privado": "SIM" if item.secreto else "NÃO",
            "Descrição": item.desc_pt
        })
    df = pd.DataFrame(dados_dict)

    # Mostra a tabela INTERATIVA (dá para ordenar e dar zoom)
    st.dataframe(df, use_container_width=True)

    # Botão de Download Real
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Relatório em Excel (CSV)",
        data=csv,
        file_name="relatorio_chapada.csv",
        mime="text/csv",
    )

elif opcao == "🗺️ Mapa via Satélite":
    st.subheader("Localização em Tempo Real")

    # Preparando dados para o Mapa (O Streamlit exige colunas 'lat' e 'lon')
    mapa_dados = []
    for item in catalogo:
        mapa_dados.append({
            "lat": item.gps[0],
            "lon": item.gps[1],
            "nome": item.nome
        })
    df_mapa = pd.DataFrame(mapa_dados)

    # O MAPA MÁGICO
    st.map(df_mapa, zoom=9)
    st.caption("Dados baseados nas coordenadas GPS cadastradas.")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.text("Desenvolvido por Calebe Eng.")