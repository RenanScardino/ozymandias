# 🏛️ Ozymandias — Darkweb Intelligence Crawler

> “My name is Ozymandias, King of Kings; Look on my Works, ye Mighty, and despair!”

Ozymandias é um projeto de OSINT para explorar a rede Onion com eficiência, segurança e profundidade. Reúne busca multi‑engine, extração resiliente de links .onion, enriquecimento paralelo e visualização em dashboard — tudo com persistência e memória para evoluir continuamente. 🔎🕵️‍♂️

## 💡 Por que Ozymandias
- 🔍 Integra múltiplos buscadores e agrega resultados relevantes
- 🧠 Analisa termos em título, meta e corpo, priorizando contexto útil
- 🕸️ Extrai links .onion mesmo quando estão ofuscados/redirecionados
- ⚙️ Aprende quais hosts .onion de cada motor funcionam melhor e se adapta
- 📚 Deduplica e consolida resultados para acompanhamento contínuo

## 🚀 Recursos Principais
- 🔎 Busca multi‑engine (parsers dedicados e genéricos)
- ⚡ Enriquecimento paralelo de conteúdo e análise de termos
- 🌐 Agregador externo com buscadores adicionais
- 📊 Persistência em Excel e resumo Markdown opcional
- 🖥️ Dashboard (Streamlit) com controle da porta SOCKS e logs

## ⚡ Comece Rápido
- Pré‑requisitos: Python 3.10+, Tor (Browser no Windows, serviço no Linux), pip
- 🪟 Windows:
  - Instale o Tor Browser e mantenha‑o aberto (porta SOCKS 9150)
  - pip install -r requirements.txt
- 🐧 Kali/Debian:
  - chmod +x setup_kali.sh && ./setup_kali.sh
  - source venv/bin/activate

## 🖥️ Execução (Dashboard)
- python -m streamlit run dashboard.py
- Na barra lateral:
  - 🔌 Defina a Porta SOCKS do Tor (9150 Windows / 9050 Linux)
  - 🧩 Informe o termo e o modo de execução
  - 📈 Acompanhe dados, logs e sondagem de buscadores

## 🛠️ Execução (CLI)
- Sintaxe:
  - python crawler.py -q "termo" -t 8 -p 9150 -o resumo.md
- Parâmetros:
  - 🔎 -q/--query: termo de busca
  - ⚙️ -t/--threads: número de threads para enriquecimento
  - 🔌 -p/--port: porta SOCKS do Tor (9150 Windows / 9050 Linux)
  - 📝 -o/--output: arquivo de resumo Markdown
- Sem -q: modo interativo via terminal

## 📦 Saídas e Dados
- 📊 Excel: resultados_busca_darkweb.xlsx (deduplicação por URL)
- 📝 Markdown: resumo opcional
- 🧾 Logs: pasta logs/ (varredura_YYYYmmdd_HHMMSS.log)
- 🧪 HTML de sondagem: pasta debug_html/

## 🧭 Buscadores Suportados
-  Ahmia, OnionLand, Torgle, Amnesia, Kaizer, Anima, Tornado, TorNet, Torland, FindTor, Excavator, Onionway, Tor66, OSS, Torgol, The Deep Searches

## 🧱 Arquitetura
- 🐍 crawler.py: busca principal, adaptação de motores, agregador externo, CLI
- 🖥️ dashboard.py: interface Streamlit (abas, execução do crawler/probe)
- 🔬 probe_engines.py: diagnóstico rápido dos buscadores e salvamento de HTML
- 🐧 setup_kali.sh: configuração em Kali/Linux (Tor, venv, dependências)
- 📊 resultados_busca_darkweb.xlsx: relatório consolidado
- 🗃️ engine_knowledge.json / knowledge.db: memória de hosts e base local de conhecimento

## 🧯 Solução de Problemas
- Tor não detectado:
  - 🪟 Windows: mantenha o Tor Browser aberto (porta 9150)
  - 🐧 Linux: sudo service tor start (porta 9050)
- Porta SOCKS:
  - Defina manualmente no dashboard ou via -p no CLI
- Streamlit:
  - Limpe o cache se necessário (pasta de cache do usuário)

## ⚖️ Ética e Legal
- Uso apenas para fins educacionais e de pesquisa de segurança
- Siga as leis locais e políticas institucionais
- Evite conteúdo ilegal; utilize com responsabilidade
