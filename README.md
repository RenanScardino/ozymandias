# OZYMANDIAS // DARKWEB OSINT CONSOLE
> “My name is Ozymandias, King of Kings; Look on my Works, ye Mighty, and despair!”

— STATUS: ONLINE  
— INTERFACE: HUD  
— DOMÍNIO: Onion Network  

Ozymandias é um sistema de inteligência para coleta e análise na rede Onion. Opera múltiplos motores de busca, extrai links com resiliência, enriquece conteúdo, registra evidências e aprende com os endpoints que funcionam. Tudo guiado por um console HUD com telemetria, logs e dados consolidados.

## BOOT/INIT
- Requisitos: Python 3.10+, Tor (Browser no Windows / serviço no Linux), pip
- Windows:
  - Instale e mantenha Tor Browser aberto (SOCKS 9150)
  - pip install -r requirements.txt
- Kali/Debian:
  - chmod +x setup_kali.sh && ./setup_kali.sh
  - source venv/bin/activate

## SUBSYSTEMS
- Busca multi‑engine (parsers dedicados e genéricos)
- Descoberta automática de buscadores .onion (-D)
- Memória de hosts responsivos (knowledge.db)
- Enriquecimento paralelo e ranking por relevância
- Agregador externo de motores adicionais
- Dashboard HUD (Streamlit) com abas e controle de SOCKS
- Persistência em Excel e resumo Markdown

## OPERATIONS
- Dashboard:
  - python -m streamlit run dashboard.py
  - Ajuste Porta SOCKS (9150 Windows / 9050 Linux), termo de busca, threads e modo
  - Visualize HUD, Scanner, Dados, Logs e Sondagem
- CLI:
  - python crawler.py -q "termo" -t 8 -p 9150 -o resumo.md -D
  - Parâmetros:
    - -q/--query: termo
    - -t/--threads: threads de enriquecimento
    - -p/--port: porta SOCKS
    - -o/--output: arquivo de resumo (md)
    - -D/--discover: habilita descoberta de novos motores
  - Sem -q: modo interativo

## DISCOVERY MODE
- Coleta hosts .onion a partir de fontes públicas
- Gera templates de busca e valida endpoints com socks5h
- Atualiza knowledge.db com sucesso/falha por host/motor
- Integra endpoints válidos no ciclo de busca sem interromper execução

## DATA CHANNELS
- results: resultados_busca_darkweb.xlsx (deduplicação por URL)
- knowledge: knowledge.db (engines, endpoints, keywords)
- logs: logs/varredura_YYYYmmdd_HHMMSS.log
- probe: debug_html/*.html
- summaries: summary_*.md e/ou -o resumo.md

## ARCHITECTURE
- crawler.py: núcleo de busca, adaptação, agregador, CLI e descoberta
- dashboard.py: HUD/Streamlit (execução, visualização e controle)
- probe_engines.py: diagnóstico/sondagem e salvamento de HTML
- setup_kali.sh: provisionamento (Tor, venv, deps)
- engine_knowledge.json / knowledge.db: base de memória local

## HUD/TABS
- 🧭 HUD: métricas, links por termo, por motor, por data
- 🛰️ Scanner: tail de logs, auto‑refresh e abertura de pasta
- 📂 Dados: filtro por palavra‑chave/motor, exportação Excel
- 📝 Logs: seleção de arquivos, auto‑refresh, limpeza
- 🧪 Buscadores: resultados de sondagem (debug_html)
- 📄 Resumos: leitura/exports de summary_*.md e arquivos .md

## PROTOCOLS
- “Aqueça” o circuito Tor abrindo um .onion no navegador
- Ajuste threads conforme estabilidade; evite concorrência agressiva
- Use socks5h, timeouts razoáveis e pausas aleatórias entre páginas
- Detecta Porta SOCKS automaticamente; aceita override manual

## DIAGNOSTICS
- Sondagem:
  - python probe_engines.py
  - Gera HTML em debug_html para inspeção de motores
- Logs:
  - Consulte varredura_*.log no HUD; use auto‑refresh
- Desconexões:
  - Ative -D para buscar endpoints alternativos e novos motores

## FAILSAFE
- Deduplicação por URL no relatório
- Fallback por formulário para motores com variações de HTML
- Registro persistente de links e endpoints (SQLite)
- Continuidade mesmo com timeouts e falhas ocasionais

## ETHICS
- Uso educacional e pesquisa de segurança
- Respeite leis e políticas da sua jurisdição
- Evite conteúdo ilegal; opere com responsabilidade
