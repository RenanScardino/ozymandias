import streamlit as st
import pandas as pd
import plotly.express as px
import os
import subprocess
import time
import socket
from datetime import datetime
import sys
import glob
import pathlib
import shutil

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Darkweb Intelligence", page_icon="🕵️‍♂️", layout="wide", initial_sidebar_state="expanded")

# --- ESTILIZAÇÃO CSS AVANÇADA ---
st.markdown("""
<style>
.stApp { background-color: #0E1117; }
div[data-testid="stMetricValue"] { font-size: 24px; color: #00FF41; font-weight: bold; }
h1, h2, h3 { font-family: 'Courier New', Courier, monospace; color: #E0E0E0; }
.stButton>button { border-radius: 5px; font-weight: bold; border: 1px solid #333; transition: all 0.3s ease; }
.stButton>button:hover { border-color: #00FF41; color: #00FF41; }
.stDataFrame { border: 1px solid #333; border-radius: 5px; }
[data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #333; }
.stTabs [data-baseweb="tab-list"] { gap: 24px; }
.stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; gap: 1px; padding-top: 10px; padding-bottom: 10px; }
.stTabs [aria-selected="true"] { background-color: #1E1E1E; color: #00FF41; border-bottom: 2px solid #00FF41; }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÕES AUXILIARES ---

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

def load_data(file_path):
    if not os.path.exists(file_path):
        return None, "Arquivo não encontrado."
    
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            return pd.DataFrame(), "Arquivo vazio."
        
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            
        return df, None
    except Exception as e:
        return None, str(e)
def list_logs():
    os.makedirs("logs", exist_ok=True)
    files = sorted(glob.glob("logs/varredura_*.log"))
    return files
def read_log_tail(path, max_chars=8000):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
        return data[-max_chars:]
    except:
        return ""
def start_crawler(term, tor_port, mode="console", manual_port=None):
    if (not tor_port and not manual_port) or not term:
        return False, "Tor ou termo inválido"
    try:
        py = sys.executable or ("python" if os.name == 'nt' else "python3")
        args = [py, "crawler.py", term] + ([str(manual_port)] if manual_port else [])
        if os.name == 'nt':
            if mode == "console":
                subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            if mode == "console":
                term_escaped = term.replace("'", "'\\''")
                extra = f" {manual_port}" if manual_port else ""
                cmd = f"{py} crawler.py '{term_escaped}'{extra}; exec bash"
                terminal_cmds = [
                    ["x-terminal-emulator", "-e", "bash", "-lc", cmd],
                    ["gnome-terminal", "--", "bash", "-lc", cmd],
                    ["konsole", "-e", "bash", "-lc", cmd],
                    ["xterm", "-e", f"bash -lc \"{cmd}\""],
                ]
                launched = False
                for tc in terminal_cmds:
                    if shutil.which(tc[0]):
                        subprocess.Popen(tc)
                        launched = True
                        break
                if not launched:
                    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True, None
    except Exception as e:
        return False, str(e)
def run_probe():
    try:
        py = sys.executable or ("python" if os.name == 'nt' else "python3")
        if os.name == 'nt':
            subprocess.Popen([py, "probe_engines.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            cmd = f"{py} probe_engines.py; exec bash"
            terminal_cmds = [
                ["x-terminal-emulator", "-e", "bash", "-lc", cmd],
                ["gnome-terminal", "--", "bash", "-lc", cmd],
                ["konsole", "-e", "bash", "-lc", cmd],
                ["xterm", "-e", f"bash -lc \"{cmd}\""],
            ]
            launched = False
            for tc in terminal_cmds:
                if shutil.which(tc[0]):
                    subprocess.Popen(tc)
                    launched = True
                    break
            if not launched:
                subprocess.Popen([py, "probe_engines.py"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True, None
    except Exception as e:
        return False, str(e)
def summarize_probe():
    os.makedirs("debug_html", exist_ok=True)
    files = sorted(glob.glob("debug_html/*.html"))
    names = [pathlib.Path(f).stem for f in files]
    return names

# --- SIDEBAR ---

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Tor-logo-2011-flat.svg/1200px-Tor-logo-2011-flat.svg.png", width=100)
    st.title("Controle")
    st.markdown("---")
    tor_port = check_tor_port()
    st.subheader("📡 Status da Rede")
    if tor_port:
        st.success(f"TOR CONECTADO (Porta {tor_port})")
    else:
        st.error("TOR DESCONECTADO")
        st.warning("Abra o Tor Browser ou inicie o serviço Tor.")
    st.markdown("---")
    st.subheader("🚀 Execução do Crawler")
    search_term = st.text_input("Termo Alvo", placeholder="Ex: passaportes, cpf...")
    manual_port_str = st.text_input("Porta SOCKS do Tor (opcional)", value=str(tor_port) if tor_port else "")
    manual_port = int(manual_port_str) if manual_port_str.strip().isdigit() else None
    run_mode = st.radio("Modo de execução no Windows", ["Console externo", "Background"], index=0 if os.name == 'nt' else 0)
    if st.button("Iniciar"):
        if not tor_port and not manual_port:
            st.error("Conecte ao Tor primeiro.")
        elif not search_term:
            st.warning("Digite um termo para buscar.")
        else:
            ok, err = start_crawler(search_term, tor_port, mode="console" if run_mode == "Console externo" else "background", manual_port=manual_port)
            if ok:
                st.success("Crawler iniciado")
            else:
                st.error(f"Falha ao iniciar: {err}")
    st.markdown("---")
    if st.button("Sondar Buscadores"):
        ok, err = run_probe()
        if ok:
            st.info("Sondagem iniciada")
        else:
            st.error(f"Falha na sondagem: {err}")
    st.caption(f"Versão 3.0 | SO: {os.name.upper()}")

# --- ÁREA PRINCIPAL ---
st.title("🕵️‍♂️ Darkweb Intelligence")
st.markdown("Monitoramento e análise na rede Onion")

# Carregar Dados
RESULTS_FILE = "resultados_busca_darkweb.xlsx"
df, error_msg = load_data(RESULTS_FILE)

# Layout de Abas
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🔎 Dados", "📝 Logs", "🧪 Buscadores"])

# --- ABA 1: VISÃO GERAL ---
with tab1:
    if df is not None and not df.empty:
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
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("📈 Links por Termo")
            if 'Termo Pesquisado' in df.columns:
                term_counts = df['Termo Pesquisado'].value_counts().reset_index()
                term_counts.columns = ['Termo', 'Contagem']
                fig_bar = px.bar(term_counts, x='Termo', y='Contagem', text='Contagem', color='Contagem', color_continuous_scale=['#004d1a', '#00ff41'], template='plotly_dark')
                fig_bar.update_traces(textposition='outside')
                fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_bar, use_container_width=True)
        with c2:
            st.subheader("🎯 Eficiência dos Buscadores")
            if 'Motor de Busca' in df.columns:
                engine_counts = df['Motor de Busca'].value_counts().reset_index()
                engine_counts.columns = ['Motor', 'Links']
                fig_pie = px.pie(engine_counts, values='Links', names='Motor', hole=0.4, color_discrete_sequence=px.colors.sequential.Greens_r, template='plotly_dark')
                fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)
    elif df is not None and df.empty:
        st.info("O banco de dados existe, mas está vazio. Inicie uma busca para coletar dados.")
    else:
        st.warning(f"Banco de dados não encontrado ou inacessível. ({error_msg})")
        st.markdown("👉 Inicie o Crawler no menu lateral para gerar o primeiro relatório.")

# --- ABA 2: EXPLORADOR DE DADOS ---
with tab2:
    st.subheader("📂 Base de Dados")
    if df is not None and not df.empty:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            search_query = st.text_input("Filtrar por palavra-chave (URL, Título, Snippet, Contextos):")
        with col_f2:
            if 'Motor de Busca' in df.columns:
                all_engines = ['Todos'] + list(df['Motor de Busca'].unique())
                engine_filter = st.selectbox("Filtrar por Buscador:", all_engines)
            else:
                engine_filter = 'Todos'
        df_filtered = df.copy()
        if search_query:
            df_filtered = df_filtered[
                df_filtered.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            ]
        if engine_filter != 'Todos':
            df_filtered = df_filtered[df_filtered['Motor de Busca'] == engine_filter]
        st.markdown(f"Exibindo {len(df_filtered)} resultados")
        st.dataframe(
            df_filtered,
            column_config={
                "URL": st.column_config.LinkColumn("Link Onion", display_text="Abrir Link"),
                "Snippet": st.column_config.TextColumn("Trecho", width="large"),
                "Contextos": st.column_config.TextColumn("Contextos", width="large"),
                "Data": st.column_config.DatetimeColumn("Data", format="DD/MM/YYYY HH:mm"),
            },
            use_container_width=True,
            height=600
        )
        with open(RESULTS_FILE, "rb") as f:
            st.download_button(
                label="📥 Exportar (Excel)",
                data=f.read(),
                file_name=f"relatorio_darkweb_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key='download-btn'
            )
    else:
        st.info("Nenhum dado disponível para visualização.")

# --- ABA 3: FERRAMENTAS ---
with tab3:
    st.subheader("📝 Logs de Execução")
    logs = list_logs()
    if logs:
        selected_log = st.selectbox("Selecione o log", logs, index=len(logs)-1)
        col_l1, col_l2 = st.columns([3,1])
        with col_l1:
            st.code(read_log_tail(selected_log, 12000), language="text")
        with col_l2:
            auto_refresh = st.checkbox("Auto-Refresh 10s")
            if st.button("Abrir pasta de logs"):
                path = os.path.abspath("logs")
                if os.name == 'nt':
                    os.startfile(path)
                else:
                    opener = shutil.which("xdg-open") or shutil.which("gnome-open")
                    if opener:
                        subprocess.Popen([opener, path])
            if auto_refresh:
                time.sleep(10)
                st.rerun()
    else:
        st.info("Nenhum log disponível.")
    st.markdown("---")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("Limpar logs"):
            try:
                for f in logs:
                    os.remove(f)
                st.success("Logs removidos")
            except Exception as e:
                st.error(f"Falha: {e}")
    with col_b2:
        if st.button("Limpar relatório"):
            try:
                if os.path.exists(RESULTS_FILE):
                    os.remove(RESULTS_FILE)
                st.success("Relatório removido")
            except Exception as e:
                st.error(f"Falha: {e}")
with tab4:
    st.subheader("🧪 Sondagem de Buscadores")
    col_p1, col_p2 = st.columns([2,1])
    with col_p1:
        names = summarize_probe()
        if names:
            df_probe = pd.DataFrame({"Buscador": names, "Status": ["OK"]*len(names)})
            st.dataframe(df_probe, use_container_width=True, height=400)
        else:
            st.info("Nenhum resultado de sondagem encontrado.")
    with col_p2:
        if st.button("Abrir pasta debug_html"):
            path = os.path.abspath("debug_html")
            if os.name == 'nt':
                os.startfile(path)
            else:
                opener = shutil.which("xdg-open") or shutil.which("gnome-open")
                if opener:
                    subprocess.Popen([opener, path])
