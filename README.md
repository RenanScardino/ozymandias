# 🕵️ Darkweb Intelligence Monitor

Ferramenta avançada de **Threat Intelligence** (OSINT) para monitoramento automatizado de ameaças e vazamento de dados na Darkweb (Rede Onion). O sistema realiza buscas profundas, detecta links, extrai snippets e gera relatórios consolidados em tempo real através de um dashboard interativo.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Tor](https://img.shields.io/badge/Network-Tor%20(Onion)-purple)
![Kali Linux](https://img.shields.io/badge/Supported-Kali%20Linux-black)
![Windows](https://img.shields.io/badge/Supported-Windows-blue)

---

## 🚀 Funcionalidades Principais

*   **🕵️ Busca Multi-Engine**: Varre simultaneamente **12 motores de busca** da Darkweb para máxima cobertura.
*   **📑 Paginação Automática**: Diferencial exclusivo que percorre múltiplas páginas de resultados (Next/Próxima), não parando apenas na primeira página.
*   **📡 Conexão Tor Híbrida**: Detecta e utiliza automaticamente o **Tor Browser** (Windows/Porta 9150) ou **Serviço Tor** (Linux/Porta 9050).
*   **📊 Dashboard Profissional**: Interface gráfica (Streamlit) "Dark Mode" com métricas, gráficos e filtros de dados em tempo real.
*   **🐢 Comportamento Humano**: Pausas aleatórias e rotação de User-Agents para evitar bloqueios e sobrecarga na rede Tor.
*   **💾 Persistência de Dados**: Salva histórico de buscas em Excel, com deduplicação inteligente de links.

---

## 🔎 Motores de Busca Suportados

O crawler realiza varreduras nos seguintes indexadores da rede Onion:

| Motor | URL Onion (Truncada) | Tipo |
| :--- | :--- | :--- |
| **Ahmia** | `juhanurmi...onion` | Indexador robusto e limpo |
| **Torch** | `xmh57jrk...onion` | Um dos mais antigos e vastos |
| **Haystak** | `haystak5...onion` | Famoso por indexar bilhões de páginas |
| **OnionLand** | `3bbad7f...onion` | Buscador rápido e popular |
| **TorDex** | `tordexu7...onion` | Focado em mercados e fóruns |
| **DarknetSearch** | `darkent7...onion` | Buscador geral |
| **Tor66** | `tor66sew...onion` | Diretório e busca |
| **OnionRealm** | `orealmvx...onion` | Motor de busca profundo |
| **Excavator** | `2fd6cemt...onion` | Indexador de conteúdo oculto |
| **TthSearch** | `tth4he7k...onion` | Busca textual simples |
| **Labyrinth** | `labyrint...onion` | Busca categorizada |
| **DeepSearch** | `dgwq7uzh...onion` | Buscador PHP clássico |

---

## 📂 Estrutura do Projeto

```bash
Darkweb/
├── crawler.py          # 🧠 CÉREBRO: Script de busca, paginação e conexão Tor
├── dashboard.py        # 🖥️ VISUAL: Interface gráfica Streamlit v2.0
├── probe_engines.py    # 🛠️ DIAGNÓSTICO: Testa quais buscadores estão online
├── setup_kali.sh       # 🐧 INSTALADOR: Script de configuração automática para Kali
├── requirements.txt    # 📦 DEPENDÊNCIAS: Lista de bibliotecas Python
└── resultados_busca_darkweb.xlsx # 📄 DADOS: Relatório gerado (criado após uso)
```

---

## 💻 Instalação e Uso

### 🐧 Opção 1: Kali Linux / Debian (Recomendado)

O projeto inclui um script de "instalação em um clique" que configura o Tor e o ambiente Python.

1.  **Instalação**:
    Abra o terminal na pasta do projeto e rode:
    ```bash
    chmod +x setup_kali.sh
    ./setup_kali.sh
    ```
    *O script pedirá sua senha `sudo` para instalar o serviço Tor.*

2.  **Execução**:
    Ative o ambiente virtual e inicie o dashboard:
    ```bash
    source venv/bin/activate
    streamlit run dashboard.py
    ```
    *O navegador abrirá. Use a barra lateral para inserir um termo e iniciar a busca.*

### 🪟 Opção 2: Windows

1.  **Pré-requisito**: Baixe e instale o [Tor Browser](https://www.torproject.org/download/).
    *   **IMPORTANTE**: Deixe o Tor Browser **ABERTO** enquanto usa a ferramenta (ele fornece a conexão na porta 9150).

2.  **Instalação**:
    Abra o terminal (CMD ou PowerShell) na pasta e instale as dependências:
    ```powershell
    pip install -r requirements.txt
    ```

3.  **Execução**:
    ```powershell
    streamlit run dashboard.py
    ```

---

## 🖥️ Guia do Dashboard

1.  **Status do Tor**: Verifique no menu lateral se aparece **"✅ TOR CONECTADO"**.
    *   Se estiver vermelho, verifique se o Tor Browser (Windows) ou serviço Tor (Linux) está rodando.
2.  **Busca**:
    *   Digite um termo (ex: `passport`, `leak`, `cpf`) no campo de busca lateral.
    *   Clique em **"🚀 Executar Crawler"**.
3.  **Monitoramento**:
    *   Uma janela preta (terminal) se abrirá mostrando o progresso detalhado: `> Pesquisando 'termo' no Ahmia...`.
    *   Aguarde a finalização.
4.  **Análise**:
    *   O dashboard carrega os dados automaticamente. Use a aba **"🔎 Explorador de Dados"** para filtrar e exportar os resultados.

---

## ⚠️ Aviso Legal e Ética

Esta ferramenta foi desenvolvida estritamente para fins de **Educação**, **Pesquisa de Segurança** e **Threat Intelligence**.

*   **NÃO** utilize para acessar conteúdo ilegal ou proibido.
*   **NÃO** utilize para assediar, atacar ou coletar dados de terceiros sem autorização.
*   O acesso à Darkweb pode expor seu computador a riscos. Use com responsabilidade.
*   O autor não se responsabiliza pelo mau uso desta ferramenta.

---

**Desenvolvido com Python 🐍 e Streamlit 🔴**
