import streamlit as st
import pandas as pd

# ==============================================================================
# 1. A ENGENHARIA (MOLDE INTEGRADO) - Resolve o erro de dominios.py
# ==============================================================================
class PontoTuristico:
    def __init__(self, nome, tipo, gps, desc_pt, desc_en, eh_secreto):
        self.nome = nome
        self.tipo = tipo
        self.gps = gps  # Tupla (lat, lon)
        self.desc_pt = desc_pt
        self.desc_en = desc_en
        self.secreto = eh_secreto

# ==============================================================================
# 2. O BANCO DE DADOS (LEITURA DO CSV)
# ==============================================================================
@st.cache_data
def carregar_dados():
    try:
        df_csv = pd.read_csv('pontos.csv')
        lista_pontos = []
        for _, row in df_csv.iterrows():
            p = PontoTuristico(
                row['nome'], row['tipo'], 
                (row['lat'], row['lon']), 
                row['desc_pt'], row['desc_en'], row['eh_secreto']
            )
            lista_pontos.append(p)
        return lista_pontos
    except Exception as e:
        st.error(f"Erro ao ler pontos.csv: {e}")
        return []

catalogo = carregar_dados()

# ==============================================================================
# 3. INTERFACE (O SITE)
# ==============================================================================
st.title("🌵 Guia Chapada das Mesas")

if not catalogo:
    st.warning("Aguardando dados do arquivo pontos.csv...")
else:
    opcao = st.sidebar.radio("Navegação", ["📊 Relatório", "🗺️ Mapa"])
    
    if opcao == "📊 Relatório":
        st.header("Relatório de Locais")
        dados = [{"Nome": i.nome, "Tipo": i.tipo, "Descrição": i.desc_pt} for i in catalogo]
        st.dataframe(pd.DataFrame(dados), use_container_width=True)
        
    elif opcao == "🗺️ Mapa":
        st.header("Localização Satélite")
        dados_mapa = [{"lat": i.gps[0], "lon": i.gps[1]} for i in catalogo]
        st.map(pd.DataFrame(dados_mapa))

st.sidebar.markdown("---")
st.sidebar.write("Engenharia: Calebe")
