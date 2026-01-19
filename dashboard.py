import streamlit as st
import pandas as pd
import plotly.express as px
import os
import subprocess
import time
import socket
from datetime import datetime
import sys

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Darkweb Intelligence Dashboard",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS AVANÇADA ---
st.markdown("""
<style>
    /* Fundo geral e cores principais */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Cards de métricas */
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #00FF41; /* Hacker Green */
        font-weight: bold;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Courier New', Courier, monospace;
        color: #E0E0E0;
    }
    
    /* Botões */
    .stButton>button {
        border-radius: 5px;
        font-weight: bold;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #00FF41;
        color: #00FF41;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #333;
        border-radius: 5px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #333;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E1E1E;
        color: #00FF41;
        border-bottom: 2px solid #00FF41;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÕES AUXILIARES ---

def check_tor_port():
    """Verifica se a porta do Tor está aberta."""
    ports = [9150, 9050]
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                s.close()
                return port
        except:
            pass
    return None

def load_data(file_path):
    """Carrega os dados do Excel com tratamento de erros."""
    if not os.path.exists(file_path):
        return None, "Arquivo não encontrado."
    
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            return pd.DataFrame(), "Arquivo vazio."
        
        # Garantir conversão de data
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            
        return df, None
    except Exception as e:
        return None, str(e)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Tor-logo-2011-flat.svg/1200px-Tor-logo-2011-flat.svg.png", width=100)
    st.title("Sistema de Controle")
    st.markdown("---")
    
    # Status do Tor
    tor_port = check_tor_port()
    st.subheader("📡 Status da Rede")
    if tor_port:
        st.success(f"TOR CONECTADO (Porta {tor_port})")
    else:
        st.error("TOR DESCONECTADO")
        st.warning("Abra o Tor Browser ou inicie o serviço Tor.")

    st.markdown("---")
    
    # Controle do Crawler
    st.subheader("🚀 Iniciar Nova Busca")
    search_term = st.text_input("Termo Alvo", placeholder="Ex: passaportes, cpf...")
    
    if st.button("Executar Crawler", use_container_width=True):
        if not tor_port:
            st.error("ERRO: Conecte ao Tor primeiro.")
        elif not search_term:
            st.warning("Digite um termo para buscar.")
        else:
            status_placeholder = st.empty()
            status_placeholder.info(f"🚀 Iniciando busca por: {search_term}...")
            
            try:
                # Comando compatível com SO
                if os.name == 'nt': # Windows
                    subprocess.Popen(["python", "crawler.py", search_term], creationflags=subprocess.CREATE_NEW_CONSOLE)
                else: # Linux
                    term_escaped = search_term.replace("'", "'\\''")
                    # Tenta abrir terminal, fallback para background
                    try:
                        cmd = f"python3 crawler.py '{term_escaped}'; exec bash"
                        subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", cmd])
                    except FileNotFoundError:
                        subprocess.Popen(["python3", "crawler.py", search_term])
                
                status_placeholder.success("✅ Crawler Iniciado em Terminal Externo!")
                time.sleep(3)
                status_placeholder.empty()
                
            except Exception as e:
                st.error(f"Falha ao iniciar: {e}")

    st.markdown("---")
    st.caption(f"Versão 2.0 | SO: {os.name.upper()}")

# --- ÁREA PRINCIPAL ---
st.title("🕵️‍♂️ Darkweb Intelligence Dashboard")
st.markdown("Monitoramento e análise de ameaças em tempo real na rede Onion.")

# Carregar Dados
RESULTS_FILE = "resultados_busca_darkweb.xlsx"
df, error_msg = load_data(RESULTS_FILE)

# Layout de Abas
tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "🔎 Explorador de Dados", "⚙️ Ferramentas"])

# --- ABA 1: VISÃO GERAL ---
with tab1:
    if df is not None and not df.empty:
        # Métricas de Topo
        col1, col2, col3, col4 = st.columns(4)
        
        total_links = len(df)
        unique_domains = df['URL'].apply(lambda x: x.split('.onion')[0] + '.onion' if isinstance(x, str) and '.onion' in x else 'Outro').nunique()
        top_engine = df['Motor de Busca'].mode()[0] if 'Motor de Busca' in df.columns else "N/A"
        last_update = df['Data'].max().strftime('%d/%m %H:%M') if 'Data' in df.columns else "N/A"
        
        col1.metric("Total de Links", total_links, delta_color="off")
        col2.metric("Domínios Únicos", unique_domains, delta_color="off")
        col3.metric("Melhor Buscador", top_engine, delta_color="off")
        col4.metric("Última Captura", last_update, delta_color="off")
        
        st.markdown("---")
        
        # Gráficos
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("📈 Atividade de Busca (Links por Termo)")
            if 'Termo Pesquisado' in df.columns:
                term_counts = df['Termo Pesquisado'].value_counts().reset_index()
                term_counts.columns = ['Termo', 'Contagem']
                fig_bar = px.bar(term_counts, x='Termo', y='Contagem', 
                                 text='Contagem', color='Contagem',
                                 color_continuous_scale=['#004d1a', '#00ff41'],
                                 template='plotly_dark')
                fig_bar.update_traces(textposition='outside')
                fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with c2:
            st.subheader("🎯 Eficiência dos Buscadores")
            if 'Motor de Busca' in df.columns:
                engine_counts = df['Motor de Busca'].value_counts().reset_index()
                engine_counts.columns = ['Motor', 'Links']
                fig_pie = px.pie(engine_counts, values='Links', names='Motor', 
                                 hole=0.4, color_discrete_sequence=px.colors.sequential.Greens_r,
                                 template='plotly_dark')
                fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)

    elif df is not None and df.empty:
        st.info("O banco de dados existe, mas está vazio. Inicie uma busca para coletar dados.")
    else:
        st.warning(f"Banco de dados não encontrado ou inacessível. ({error_msg})")
        st.markdown("### 👉 Inicie o Crawler no menu lateral para gerar o primeiro relatório.")

# --- ABA 2: EXPLORADOR DE DADOS ---
with tab2:
    st.subheader("📂 Base de Dados Completa")
    
    if df is not None and not df.empty:
        # Filtros Dinâmicos
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            search_query = st.text_input("Filtrar por palavra-chave (URL, Título ou Snippet):")
        with col_f2:
            if 'Motor de Busca' in df.columns:
                all_engines = ['Todos'] + list(df['Motor de Busca'].unique())
                engine_filter = st.selectbox("Filtrar por Buscador:", all_engines)
            else:
                engine_filter = 'Todos'
        
        # Aplicar Filtros
        df_filtered = df.copy()
        
        if search_query:
            df_filtered = df_filtered[
                df_filtered.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            ]
            
        if engine_filter != 'Todos':
            df_filtered = df_filtered[df_filtered['Motor de Busca'] == engine_filter]
            
        st.markdown(f"**Exibindo {len(df_filtered)} resultados**")
        
        # Tabela Interativa
        st.dataframe(
            df_filtered,
            column_config={
                "URL": st.column_config.LinkColumn("Link Onion", display_text="Abrir Link"),
                "Snippet": st.column_config.TextColumn("Trecho", width="large"),
                "Data": st.column_config.DatetimeColumn("Data", format="DD/MM/YYYY HH:mm"),
            },
            use_container_width=True,
            height=600
        )
        
        # Botão Download
        with open(RESULTS_FILE, "rb") as f:
            st.download_button(
                label="📥 Exportar Dados Filtrados (Excel)",
                data=f.read(),
                file_name=f"relatorio_darkweb_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key='download-btn'
            )
            
    else:
        st.info("Nenhum dado disponível para visualização.")

# --- ABA 3: FERRAMENTAS ---
with tab3:
    st.subheader("🛠️ Manutenção e Configurações")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("### 🗑️ Limpeza de Dados")
        st.warning("Atenção: Esta ação é irreversível.")
        if st.button("Limpar Banco de Dados Completo"):
            if os.path.exists(RESULTS_FILE):
                try:
                    os.remove(RESULTS_FILE)
                    st.success("Banco de dados deletado com sucesso! Atualize a página.")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao deletar: {e}")
            else:
                st.info("Nenhum arquivo para deletar.")
                
    with col_t2:
        st.markdown("### 🔄 Atualização Automática")
        auto_refresh = st.checkbox("Ativar Auto-Refresh da Página (15s)")
        if auto_refresh:
            time.sleep(15)
            st.rerun()

