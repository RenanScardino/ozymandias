# 🏛️ Ozymandias — Darkweb Intelligence Crawler

> “My name is Ozymandias, King of Kings; Look on my Works, ye Mighty, and despair!”

Ozymandias é um projeto de OSINT focado em coleta resiliente na rede Onion. Combina busca multi‑engine, extração robusta de links .onion, enriquecimento paralelo e um dashboard em estilo HUD para operar e inspecionar dados em tempo real. Mantém memória local para aprender com endpoints que funcionam e se adaptar com o tempo.

## 💡 Visão Geral
- 🔍 Integra múltiplos buscadores e agrega resultados sem duplicação
- 🧠 Analisa termos em título, meta e corpo para priorizar contexto útil
- 🕸️ Extrai links .onion mesmo com ofuscação/redirecionamento
- ⚙️ Aprende quais hosts .onion de cada motor estão estáveis e reusa
- 📚 Persiste resultados para acompanhamento contínuo e revisões

## 🚀 Recursos Principais
<<<<<<< HEAD
- 🔎 Busca multi‑engine com parsers dedicados e genéricos
- 🧭 Modo de descoberta automática de novos buscadores .onion (validação de endpoints)
- 🧠 Base de conhecimento local (knowledge.db) com sucesso/falha por motor/host
- ⚡ Enriquecimento paralelo de conteúdo e ranking por relevância
- 🌐 Agregador externo com motores adicionais quando disponíveis
=======
- 🔎 Busca multi‑engine (parsers dedicados e genéricos)
- ⚡ Enriquecimento paralelo de conteúdo e análise de termos
- 🌐 Agregador externo com buscadores adicionais
>>>>>>> a4b30e62b88d8374db43f07f4f1bd6cce15d699e
- 📊 Persistência em Excel e resumo Markdown opcional
- 🖥️ Dashboard HUD (Streamlit) com controle de porta SOCKS, abas de dados/logs e sondagem

## ⚡ Instalação
- Pré‑requisitos: Python 3.10+, Tor (Browser no Windows / serviço no Linux), pip
- 🪟 Windows:
  - Instale o Tor Browser e mantenha‑o aberto (porta SOCKS 9150)
  - pip install -r requirements.txt
- 🐧 Kali/Debian:
  - chmod +x setup_kali.sh && ./setup_kali.sh
  - source venv/bin/activate

## 🖥️ Execução (Dashboard)
- python -m streamlit run dashboard.py
- Barra lateral:
  - 🔌 Porta SOCKS do Tor (9150 Windows / 9050 Linux)
  - 🔎 Termo de busca e seleção de modo
  - 📈 Abas para HUD/Scanner/Dados/Logs/Buscadores

## 🛠️ Execução (CLI)
- Sintaxe rápida:
  - python crawler.py -q "termo" -t 8 -p 9150 -o resumo.md
- Parâmetros:
  - 🔎 -q/--query: termo de busca
  - ⚙️ -t/--threads: número de threads para enriquecimento
  - 🔌 -p/--port: porta SOCKS do Tor (9150 Windows / 9050 Linux)
  - 📝 -o/--output: arquivo de resumo Markdown
  - 🔎 -D/--discover: ativa descoberta automática de novos buscadores
- Sem -q: modo interativo via terminal

## 🧭 Modo Descoberta
- Detecta candidatos de motores .onion a partir de fontes públicas
- Extrai hosts .onion e testa padrões de URL de pesquisa por motor
- Valida endpoints usando proxies socks5h e registra sucesso/falha
- Atualiza knowledge.db para priorizar motores que comprovadamente funcionam
- Integra candidatos válidos no ciclo de busca sem interromper a execução

## 📦 Saídas e Dados
- 📊 Excel: resultados_busca_darkweb.xlsx (deduplicação por URL)
- 🧠 Base: knowledge.db (histórico de validação de motores/hosts)
- 📝 Markdown: resumo opcional
- 🧾 Logs: pasta logs/ (varredura_YYYYmmdd_HHMMSS.log)
- 🧪 HTML de sondagem: pasta debug_html/

<<<<<<< HEAD
=======
## 🧭 Buscadores Suportados
-  Ahmia, OnionLand, Torgle, Amnesia, Kaizer, Anima, Tornado, TorNet, Torland, FindTor, Excavator, Onionway, Tor66, OSS, Torgol, The Deep Searches

>>>>>>> a4b30e62b88d8374db43f07f4f1bd6cce15d699e
## 🧱 Arquitetura
- 🐍 crawler.py: busca principal, adaptação de motores, agregador externo, CLI e descoberta
- 🖥️ dashboard.py: interface Streamlit (HUD, execução do crawler/probe, visualização)
- 🔬 probe_engines.py: diagnóstico de buscadores e salvamento de HTML
- 🐧 setup_kali.sh: configuração em Kali/Linux (Tor, venv, dependências)
- 📊 resultados_busca_darkweb.xlsx: relatório consolidado
- 🗃️ engine_knowledge.json / knowledge.db: memória de hosts e base local de conhecimento

## 🧭 Buscadores (dinâmico)
- Internos e agregados variam conforme disponibilidade na rede Onion
- O projeto aprende e prioriza os que respondem com qualidade
- Alguns exemplos: Ahmia, Torch (Omega), OnionLand, Tor66, Excavator, OSS, etc.
- Observação: endpoints podem mudar; o modo descoberta ajuda a manter atual

## 🔐 Boas Práticas com Tor
- “Aqueça” o circuito abrindo qualquer site .onion no navegador
- Evite concorrência excessiva; ajuste threads conforme estabilidade da rede
- Ajuste timeouts se notar lentidão ou rotas congestionadas
- Use sempre proxies socks5h e mantenha portas corretas (9150/9050)

## 🧯 Solução de Problemas
- Tor não detectado:
  - 🪟 Windows: mantenha o Tor Browser aberto (porta 9150)
  - 🐧 Linux: sudo service tor start (porta 9050)
- Porta SOCKS:
  - Defina manualmente no dashboard ou via -p no CLI
- Streamlit:
  - Limpe o cache do usuário em caso de inconsistência visual
- Desconexões de buscadores:
  - Ative -D/--discover para buscar endpoints alternativos e motores novos
  - Utilize a sondagem para inspecionar HTML e validar acessos

## ⚖️ Ética e Legal
- Uso apenas para fins educacionais e de pesquisa de segurança
- Siga as leis locais e políticas institucionais
- Evite conteúdo ilegal; utilize com responsabilidade
