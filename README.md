# Ozymandias — Darkweb Intelligence Crawler

Ozymandias é um projeto de OSINT focado na varredura, análise e agregação de resultados na rede Onion. Ele oferece um dashboard interativo e um modo CLI eficiente, combinando busca multi‑engine, extração robusta de links .onion, enriquecimento paralelo e persistência de dados.

## Recursos
- Busca multi‑engine com parsers dedicados e genéricos
- Ahmia tratado como página única quando necessário
- Extração robusta de destinos .onion em links com redirecionamento
- Enriquecimento paralelo dos links e análise de termos (título/meta/corpo)
- Adaptação de motores: aprende hosts .onion que respondem e troca quando um falha
- Agregador externo com múltiplos buscadores adicionais em paralelo
- Persistência em Excel (deduplicação por URL) e resumo Markdown opcional
- Dashboard (Streamlit) com controle manual da porta SOCKS e visualização de dados/logs

## Buscadores Internos
- Ahmia, Torch, Haystak, OnionLand, TorDex, DarknetSearch, Tor66, OnionRealm, Excavator, TthSearch, Labyrinth, DeepSearch

## Buscadores do Agregador Externo
- Ahmia, OnionLand, Torgle, Amnesia, Kaizer, Anima, Tornado, TorNet, Torland, FindTor, Excavator, Onionway, Tor66, OSS, Torgol, The Deep Searches

## Arquitetura
- crawler.py: busca principal, adaptação de motores, agregador externo, CLI
- dashboard.py: interface Streamlit com abas, execução do crawler/probe
- probe_engines.py: diagnóstico rápido dos buscadores e salvamento de HTML
- setup_kali.sh: configuração em Kali/Linux (Tor, venv, dependências)
- resultados_busca_darkweb.xlsx: relatório consolidado
- engine_knowledge.json / knowledge.db: memória de hosts e base local de conhecimento

## Instalação
- Requisitos: Python 3.10+, Tor (Browser no Windows, serviço no Linux), pip
- Windows:
  - Instale o Tor Browser e mantenha‑o aberto (porta SOCKS 9150)
  - pip install -r requirements.txt
- Kali/Debian:
  - chmod +x setup_kali.sh && ./setup_kali.sh
  - source venv/bin/activate

## Execução do Dashboard
- Windows/Kali:
  - python -m streamlit run dashboard.py
  - Barra lateral:
    - Porta SOCKS do Tor (opcional): 9150 (Windows) ou 9050 (Linux)
    - Termo e modo de execução
  - Visualize dados, logs e sondagem de buscadores

## Execução por CLI
- Sintaxe:
  - python crawler.py -q "termo" -t 8 -p 9150 -o resumo.md
- Parâmetros:
  - -q/--query: termo de busca
  - -t/--threads: número de threads para enriquecimento
  - -p/--port: porta SOCKS do Tor (9150 Windows / 9050 Linux)
  - -o/--output: arquivo de resumo Markdown
- Sem -q: entra em modo interativo via terminal

## Saída e Logs
- Excel: resultados_busca_darkweb.xlsx (deduplicação por URL)
- Markdown: arquivo de resumo (se -o informado)
- Logs: pasta logs/ (varredura_YYYYmmdd_HHMMSS.log)
- HTML de sondagem: pasta debug_html/

## Dicas e Solução de Problemas
- Tor não detectado:
  - Windows: mantenha o Tor Browser aberto (porta 9150)
  - Linux: sudo service tor start (porta 9050)
- Porta SOCKS:
  - Defina manualmente no dashboard ou via -p no CLI
- Cache do Streamlit:
  - Remova ~/.streamlit/cache se necessário

## Ética e Legal
- Uso somente para fins educacionais e de pesquisa de segurança
- Siga as leis locais e políticas institucionais
- Evite conteúdo ilegal; utilize com responsabilidade

## O nome do projeto
- O nome deste projeto é “Ozymandias”.

## Trecho de “Ozymandias” (Percy Bysshe Shelley, 1818)
> “My name is Ozymandias, King of Kings;  
> Look on my Works, ye Mighty, and despair!”
