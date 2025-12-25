import streamlit as st
import pandas as pd

# 1. CLASSE INTEGRADA (Evita erro de dominios.py)
class PontoTuristico:
    def __init__(self, nome, tipo, gps, desc_pt, desc_en, eh_secreto):
        self.nome = nome
        self.tipo = tipo
        self.gps = gps # Tupla (lat, lon)
        self.desc_pt = desc_pt
        self.desc_en = desc_en
        self.secreto = eh_secreto

# 2. CARREGAMENTO DE DADOS
@st.cache_data
def carregar_dados():
    try:
        df_csv = pd.read_csv('pontos.csv')
        lista = []
        for _, row in df_csv.iterrows():
            p = PontoTuristico(row['nome'], row['tipo'], (row['lat'], row['lon']), 
                               row['desc_pt'], row['desc_en'], row['eh_secreto'])
            lista.append(p)
        return lista
    except:
        return []

catalogo = carregar_dados()

# 3. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Guia Chapada", page_icon="🌵", layout="wide")

# 4. BARRA LATERAL (FILTROS)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=100)
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Navegação", ["🏠 Início", "📊 Relatório", "🗺️ Mapa"])

st.sidebar.markdown("---")
st.sidebar.header("Filtros")
categorias = ["Todas"] + sorted(list(set([p.tipo for p in catalogo])))
cat_sel = st.sidebar.selectbox("Filtrar por Categoria:", categorias)

# 5. LÓGICA DE FILTRAGEM
lista_filtrada = [p for p in catalogo if cat_sel == "Todas" or p.tipo == cat_sel]

# 6. TELAS
st.title("🌵 Guia Oficial: Chapada das Mesas")

if opcao == "🏠 Início":
    col1, col2 = st.columns(2)
    col1.metric("Locais Cadastrados", len(catalogo))
    col2.metric("Resultados do Filtro", len(lista_filtrada))
    st.info("Bem-vindo! Use o menu ao lado para explorar a região.")

elif opcao == "📊 Relatório":
    st.header("📊 Tabela de Dados")
    if lista_filtrada:
        dados_tab = [{"Nome": i.nome, "Tipo": i.tipo, "Descrição": i.desc_pt, "Privado": i.secreto} for i in lista_filtrada]
        st.dataframe(pd.DataFrame(dados_tab), use_container_width=True)
    else:
        st.warning("Nenhum local encontrado.")

elif opcao == "🗺️ Mapa":
    st.header("🗺️ Mapa via Satélite")
    if lista_filtrada:
        mapa_df = pd.DataFrame([{"lat": i.gps[0], "lon": i.gps[1], "nome": i.nome} for i in lista_filtrada])
        st.map(mapa_df)

st.sidebar.markdown("---")
st.sidebar.text("Engenharia: Calebe")
