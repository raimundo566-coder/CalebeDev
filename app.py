# ARQUIVO: app.py
# OBJETIVO: Web App Comercial com Streamlit - Guia Chapada das Mesas
# ATUALIZAÇÃO: Unificação de Lógica e Leitura de Banco de Dados CSV

import streamlit as st
import pandas as pd
from dominios import PontoTuristico

# 1. Configuração da Página
st.set_page_config(
    page_title="Guia Oficial: Chapada das Mesas",
    page_icon="🌵",
    layout="wide"
)

# 2. O Banco de Dados (Dinamizado com CSV)
@st.cache_data
def carregar_dados():
    try:
        # Lê a planilha de pontos que deve estar na mesma pasta no GitHub
        df_csv = pd.read_csv('pontos.csv')
        lista_pontos = []
        for _, row in df_csv.iterrows():
            # Reconstrói o objeto usando a classe importada de dominios.py
            # Note: row['lat'] e row['lon'] são convertidos para a tupla item.gps
            p = PontoTuristico(
                row['nome'], 
                row['tipo'], 
                (row['lat'], row['lon']), 
                row['desc_pt'], 
                row['desc_en'], 
                row['eh_secreto']
            )
            lista_pontos.append(p)
        return lista_pontos
    except FileNotFoundError:
        # Caso o arquivo pontos.csv ainda não exista, o sistema não quebra
        return []

catalogo = carregar_dados()

# 3. Barra Lateral (Menu e FILTROS)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=100)
st.sidebar.title("Menu de Navegação")
opcao = st.sidebar.radio("Ir para:", ["🏠 Início", "📊 Relatório", "🗺️ Mapa"])

st.sidebar.markdown("---")
st.sidebar.header("Filtros de Busca")
categoria_selecionada = st.sidebar.selectbox(
    "Escolha a Categoria:",
    ["Todas", "Aventura", "Relax", "Trilha", "Gastronomia"]
)

# 4. Construção das Telas
st.title("🌵 Guia Oficial: Chapada das Mesas")
st.markdown("---")

# TELA: INÍCIO
if opcao == "🏠 Início":
    st.info("Bem-vindo ao sistema de gestão turística! Use o menu ao lado para explorar.")
    
    col1, col2 = st.columns(2)
    col1.metric("Locais Cadastrados", len(catalogo))
    col2.metric("Status do Sistema", "Online")
    
    st.write("### O que é o projeto?")
    st.write("Este sistema utiliza **Arquitetura de Software** e **IA** para organizar e facilitar o acesso aos pontos turísticos da Chapada das Mesas.")

# TELA: RELATÓRIO
elif opcao == "📊 Relatório":
    st.header("📊 Relatório Gerencial")
    
    # Lógica de Filtro
    lista_filtrada = []
    if categoria_selecionada == "Todas":
        lista_filtrada = catalogo
    else:
        for item in catalogo:
            if item.tipo == categoria_selecionada:
                lista_filtrada.append(item)
    
    if not lista_filtrada:
        st.warning("Nenhum local encontrado nesta categoria.")
    else:
        # Preparando tabela para exibição
        dados_tabela = []
        for i in lista_filtrada:
            dados_tabela.append({
                "Nome": i.nome,
                "Tipo": i.tipo,
                "Privado": "SIM" if i.secreto else "NÃO",
                "Descrição": i.desc_pt
            })
        
        df_visual = pd.DataFrame(dados_tabela)
        st.dataframe(df_visual, use_container_width=True)
        
        # Botão de Download
        csv_data = df_visual.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Relatório (CSV)",
            data=csv_data,
            file_name="relatorio_chapada.csv",
            mime="text/csv",
        )

# TELA: MAPA
elif opcao == "🗺️ Mapa":
    st.header("🗺️ Mapa de Localização")
    
    if not catalogo:
        st.error("Sem dados para exibir no mapa.")
    else:
        # Preparando dados para o Mapa (Streamlit exige colunas 'lat' e 'lon')
        mapa_dados = []
        for item in catalogo:
            mapa_dados.append({
                "lat": item.gps[0],
                "lon": item.gps[1],
                "nome": item.nome
            })
        
        df_mapa = pd.DataFrame(mapa_dados)
        st.map(df_mapa, zoom=9)
        st.caption("Coordenadas GPS extraídas do banco de dados pontos.csv")

# Rodapé Lateral
st.sidebar.markdown("---")
st.sidebar.text("Desenvolvido por Calebe Eng.")
st.sidebar.info("Fase: Nível 2 - Arquiteto")
.
