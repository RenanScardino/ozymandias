import streamlit as st
import pandas as pd
import plotly.express as px
import os
import subprocess
import time
import socket
from datetime import datetime

# Configuração da Página
st.set_page_config(
    page_title="Darkweb Monitor Dashboard",
    page_icon="🕵️",
    layout="wide"
)

# Estilização Customizada
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    h1, h2, h3 {
        color: #00FF00; /* Hacker green */
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("🕵️ Darkweb Intelligence Monitor")
st.markdown("---")

# --- SIDEBAR: CONTROLES ---
st.sidebar.header("⚙️ Painel de Controle")

# Verificação do Tor
def check_tor_port():
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

tor_port = check_tor_port()
if tor_port:
    st.sidebar.success(f"✅ Tor Detectado (Porta {tor_port})")
else:
    st.sidebar.error("❌ Tor Offline / Não Detectado")



st.sidebar.markdown("---")

# Input de Termo Único
st.sidebar.subheader("🔍 Configuração de Busca")
search_term = st.sidebar.text_input("Termo para pesquisar:", placeholder="Ex: cpf, passaporte, vazamento...")

# Botão para Rodar o Crawler
if st.sidebar.button("🚀 Iniciar Varredura (Crawler)"):
    if not tor_port:
        st.sidebar.error("Abra o Tor Browser antes de iniciar!")
    elif not search_term:
        st.sidebar.warning("⚠️ Digite um termo para pesquisar!")
    else:
        st.sidebar.info(f"Iniciando busca por '{search_term}'...")
        try:
            # Executa o script crawler.py passando o termo como argumento
            if os.name == 'nt': # Windows
                subprocess.Popen(["python", "crawler.py", search_term], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else: # Linux / Kali
                # Tenta abrir em um novo terminal
                try:
                    # Escapa o termo para evitar injeção simples no bash
                    term_escaped = search_term.replace("'", "'\\''")
                    cmd = f"python3 crawler.py '{term_escaped}'; exec bash"
                    subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", cmd])
                except FileNotFoundError:
                    # Fallback
                    subprocess.Popen(["python3", "crawler.py", search_term])
                    st.sidebar.warning("Terminal externo não encontrado. O crawler rodará em background.")
            
            st.sidebar.success("Crawler iniciado! Verifique a janela do terminal.")
        except Exception as e:
            st.sidebar.error(f"Erro ao iniciar: {e}")


# --- DASHBOARD PRINCIPAL ---

# Carregar Dados
RESULTS_FILE = "resultados_busca_darkweb.xlsx"

if os.path.exists(RESULTS_FILE):
    try:
        df = pd.read_excel(RESULTS_FILE)
        
        # Métricas Principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Total de Links Encontrados", value=len(df))
        
        with col2:
            unique_terms = df['Termo Pesquisado'].nunique() if 'Termo Pesquisado' in df.columns else 0
            st.metric(label="Termos com Resultados", value=unique_terms)
            
        with col3:
            unique_domains = df['URL'].apply(lambda x: x.split('.onion')[0] + '.onion' if '.onion' in str(x) else 'Outro').nunique()
            st.metric(label="Domínios Únicos (.onion)", value=unique_domains)
            
        with col4:
            last_update = datetime.fromtimestamp(os.path.getmtime(RESULTS_FILE)).strftime('%d/%m/%Y %H:%M')
            st.metric(label="Última Atualização", value=last_update)

        st.markdown("---")

        # Gráficos
        c1, c2 = st.columns([2, 1])

        with c1:
            st.subheader("📊 Resultados por Termo")
            if 'Termo Pesquisado' in df.columns:
                term_counts = df['Termo Pesquisado'].value_counts().reset_index()
                term_counts.columns = ['Termo', 'Contagem']
                fig_bar = px.bar(term_counts, x='Termo', y='Contagem', color='Contagem', 
                                 color_continuous_scale='Greens', template='plotly_dark')
                st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            st.subheader("🔎 Motores de Busca")
            if 'Motor de Busca' in df.columns:
                engine_counts = df['Motor de Busca'].value_counts()
                fig_pie = px.pie(values=engine_counts.values, names=engine_counts.index, 
                                 template='plotly_dark', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)

        # Tabela de Dados
        st.subheader("📄 Detalhes dos Resultados")
        
        # Filtros
        search_filter = st.text_input("Filtrar resultados (busca livre):", "")
        
        if search_filter:
            df_display = df[df.astype(str).apply(lambda x: x.str.contains(search_filter, case=False)).any(axis=1)]
        else:
            df_display = df

        st.dataframe(
            df_display,
            column_config={
                "URL": st.column_config.LinkColumn("Link Onion"),
                "Snippet": st.column_config.TextColumn("Trecho Encontrado", width="large"),
                "Data": st.column_config.DatetimeColumn("Data da Coleta", format="DD/MM/YYYY HH:mm")
            },
            use_container_width=True,
            hide_index=True
        )

        # Botões de Ação (Download / Limpar)
        col_dl, col_del = st.columns([1, 1])
        with col_dl:
            with open(RESULTS_FILE, "rb") as f:
                file_data = f.read()
                st.download_button(
                    label="📥 Baixar Relatório (Excel)",
                    data=file_data,
                    file_name="relatorio_darkweb.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        with col_del:
            if st.button("🗑️ Limpar Todos os Dados"):
                try:
                    os.remove(RESULTS_FILE)
                    st.success("Dados removidos com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao limpar dados: {e}")

    except Exception as e:
        st.error(f"Erro ao processar arquivo de dados: {e}")
else:
    st.info("👋 Bem-vindo! Ainda não há resultados para exibir.")
    st.markdown("""
    ### Como começar:
    1. Certifique-se de que o **Tor Browser** está aberto.
    2. Adicione termos de pesquisa no menu lateral.
    3. Clique em **'Iniciar Varredura'** no menu lateral.
    4. Aguarde o crawler finalizar e atualize esta página (ou clique em 'Rerun').
    """)

# Auto-refresh (opcional, pode ser pesado se o arquivo for grande)
if st.sidebar.checkbox("Atualização Automática (10s)", value=False):
    time.sleep(10)
    st.rerun()
