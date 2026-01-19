# 🕵️ Darkweb Intelligence Monitor

Uma ferramenta completa para monitoramento de ameaças e palavras-chave na Darkweb (Rede Tor). O sistema realiza buscas automatizadas em múltiplos motores de busca onion e consolida os resultados em um dashboard interativo.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Tor](https://img.shields.io/badge/Network-Tor-purple)
![Kali Linux](https://img.shields.io/badge/OS-Kali%20Linux-black)

## 🚀 Funcionalidades

- **Multi-Engine Search**: Varre múltiplos buscadores da darkweb simultaneamente (Ahmia, Torch, Haystak, OnionLand).
- **Monitoramento de Termos**: Lê uma lista de palavras-chave do arquivo `termos.xlsx`.
- **Detecção Automática**: Identifica automaticamente se você está usando o Tor Browser (porta 9150) ou o Serviço Tor (porta 9050).
- **Dashboard Visual**: Interface gráfica para visualização de métricas e gráficos.
- **Relatórios**: Exportação automática dos dados encontrados para Excel.

## 📂 Estrutura do Projeto

```
Darkweb/
├── crawler.py          # Script principal (o motor de busca)
├── dashboard.py        # Interface gráfica (Streamlit)
├── termos.xlsx         # Lista de termos a serem pesquisados (Input)
├── resultados_busca_darkweb.xlsx # Base de dados de resultados (Output)
├── setup_kali.sh       # Instalador automático para Linux/Kali
└── requirements.txt    # Dependências do projeto
```

---

## 💻 Instalação e Execução

### Opção 1: Kali Linux (Recomendado)

O projeto possui um script de instalação que configura o serviço Tor e as dependências automaticamente.

1.  **Instalação**:
    Abra o terminal na pasta do projeto e execute:
    ```bash
    chmod +x setup_kali.sh
    ./setup_kali.sh
    ```
    *Isso instalará o `tor`, criará um ambiente virtual (`venv`) e instalará as bibliotecas necessárias.*

2.  **Execução (Dashboard)**:
    Sempre que for usar, ative o ambiente e rode o dashboard:
    ```bash
    source venv/bin/activate
    streamlit run dashboard.py
    ```
    *O navegador abrirá automaticamente. Ao clicar em "Iniciar Varredura", uma nova janela de terminal se abrirá mostrando o progresso do crawler.*

### Opção 2: Windows

1.  **Pré-requisito**: Baixe e instale o [Tor Browser](https://www.torproject.org/download/). **Mantenha-o aberto** enquanto usa a ferramenta (ele fornece o proxy na porta 9150).
2.  **Instalação**:
    ```powershell
    pip install -r requirements.txt
    ```
3.  **Execução**:
    ```powershell
    streamlit run dashboard.py
    ```

---

## 🖥️ Como Usar o Dashboard

1.  Acesse `http://localhost:8501` no seu navegador (aberto automaticamente).
2.  **Menu Lateral**:
    *   **Gerenciar Termos**: Cole seus termos (um por linha) e clique em "Salvar".
    *   **Painel de Controle**: Clique em **"🚀 Iniciar Varredura"**.
3.  **Acompanhamento**:
    *   No Linux, uma janela do terminal (`x-terminal-emulator`) abrirá rodando o crawler.
    *   No Windows, uma nova janela de prompt (`cmd`) abrirá.
4.  **Resultados**:
    *   O dashboard mostrará contadores de links encontrados, gráficos de distribuição e uma tabela pesquisável com os trechos encontrados.
    *   Atualize a página (F5 ou 'R') para ver novos resultados chegando em tempo real.

## ⚠️ Aviso Legal

Esta ferramenta foi desenvolvida para fins de **pesquisa de segurança (Threat Intelligence)** e **educacionais**. 
- O acesso à Darkweb pode envolver riscos.
- Não utilize esta ferramenta para atividades ilícitas.
- O autor não se responsabiliza pelo mau uso do código.

## 🔧 Solução de Problemas (Kali Linux)

*   **Erro "x-terminal-emulator not found"**:
    Se ao clicar em iniciar nada acontecer, instale um terminal padrão ou rode o crawler manualmente:
    ```bash
    python crawler.py
    ```
*   **Erro de Permissão no Tor**:
    Se o script reclamar que o Tor não está rodando, tente reiniciar o serviço:
    ```bash
    sudo service tor restart
    ```
