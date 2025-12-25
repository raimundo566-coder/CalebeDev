import streamlit as st
import pandas as pd

# 1. MOLDURA DE DADOS
class PontoTuristico:
    def __init__(self, nome, tipo, gps, desc_pt, desc_en, eh_secreto):
        self.nome = nome
        self.tipo = tipo
        self.gps = gps 
        self.desc_pt = desc_pt
        self.desc_en = desc_en
        self.secreto = eh_secreto

# 2. CARREGAMENTO COM SISTEMA DE SEGURANÇA
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
    except Exception as e:
        # Se o CSV falhar, ele cria pontos temporários para o site não ficar vazio
        st.error(f"Erro ao carregar CSV: {e}")
        return [
            PontoTuristico("Erro de Carregamento", "Sistema", (0,0), "Verifique o arquivo pontos.csv", "Check file", False)
        ]

catalogo = carregar_dados()

# 3. INTERFACE PROFISSIONAL
st.set_page_config(page_title="Guia Chapada", page_icon="🌵", layout="wide")

st.sidebar.title("🌵 Guia Chapada")
opcao = st.sidebar.radio("Navegação", ["🏠 Início", "📊 Relatório", "🗺️ Mapa"])

# Filtro Dinâmico
categorias = ["Todas"] + sorted(list(set([p.tipo for p in catalogo])))
cat_sel = st.sidebar.selectbox("Categoria:", categorias)
lista_filtrada = [p for p in catalogo if cat_sel == "Todas" or p.tipo == cat_sel]

# 4. EXIBIÇÃO
st.title("🌵 Guia Oficial: Chapada das Mesas")

if opcao == "🏠 Início":
    col1, col2 = st.columns(2)
    col1.metric("Locais Totais", len(catalogo))
    col2.metric("Filtrados", len(lista_filtrada))
    st.info("Bem-vindo ao sistema de gestão. Selecione uma opção no menu.")

elif opcao == "📊 Relatório":
    st.header("📊 Tabela de Dados")
    dados_tab = [{"Nome": i.nome, "Tipo": i.tipo, "Descrição": i.desc_pt} for i in lista_filtrada]
    st.dataframe(pd.DataFrame(dados_tab), use_container_width=True)

elif opcao == "🗺️ Mapa":
    st.header("🗺️ Mapa de Localização")
    mapa_df = pd.DataFrame([{"lat": i.gps[0], "lon": i.gps[1]} for i in lista_filtrada])
    st.map(mapa_df)

st.sidebar.markdown("---")
st.sidebar.caption("Versão 2.1 - Engenharia Calebe")
