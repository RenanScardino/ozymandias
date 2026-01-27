#!/usr/bin/env python3
import pandas as pd
import requests
import socket
from bs4 import BeautifulSoup
from termcolor import colored
import time
import sys
import urllib.parse
import os
import random
import re
import logging
from datetime import datetime
import unicodedata

# --- CONFIGURAÇÃO ---
SEARCH_ENGINES = {
    'Ahmia': {
        'url': 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={query}',
        'selector': 'li.result'
    },
    'Torch': {
        'url': 'http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P={query}',
        'selector': 'generic' # Parser genérico
    },
    'Haystak': {
        'url': 'http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/?q={query}',
        'selector': 'generic'
    },
    'OnionLand': {
        'url': 'http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search?q={query}',
        'selector': 'generic'
    },
    'TorDex': {
        'url': 'http://tordexu73joywapk2txdr54jed4imqledpcvcuf75qsas2gwdgksvnyd.onion/search?q={query}',
        'selector': 'generic'
    },
    'DarknetSearch': {
        'url': 'http://darkent74yfc3qe7vhd2ms53ynr3l5hbjz4on2x76e7odjiyrjlirvid.onion/search?q={query}',
        'selector': 'generic'
    },
    'Tor66': {
        'url': 'http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/search?q={query}',
        'selector': 'generic'
    },
    'OnionRealm': {
        'url': 'http://orealmvxooetglfeguv2vp65a3rig2baq2ljc7jxxs4hsqsrcemkxcad.onion/search?query={query}&action=search',
        'selector': 'generic'
    },
    'Excavator': {
        'url': 'http://2fd6cemt4gmccflhm6imvdfvli3nf7zn6rfrwpsy7uhxrgbypvwf5fad.onion/search?query={query}',
        'selector': 'generic'
    },
    'TthSearch': {
        'url': 'http://tth4he7kdfmfwq2k7yaj2ggjdva7rdpbch42q6xgoorbabjeklyfbmyd.onion/search?query={query}',
        'selector': 'generic'
    },
    'Labyrinth': {
        'url': 'http://labyrinthkh3uokhu2a5nwi4e6kedmbkxar3w6vgm2ipdb7ms3zdzlad.onion/search?query={query}&lang=english&sort-by=relevant&tab=all',
        'selector': 'generic'
    },
    'DeepSearch': {
        'url': 'http://dgwq7uzh5ro2f7p34begy4kmxue5gst7lk2spxda63zkrpuegtj4opyd.onion/search.php?q={query}',
        'selector': 'generic'
    }
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
]
ENRICH_FETCH_LIMIT = 15
LOGGER = None
LOG_FILE = None

def init_logger():
    global LOGGER, LOG_FILE
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs('logs', exist_ok=True)
    LOG_FILE = os.path.join('logs', f"varredura_{ts}.log")
    LOGGER = logging.getLogger("crawler")
    LOGGER.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(formatter)
    if not LOGGER.handlers:
        LOGGER.addHandler(fh)
    return LOGGER, LOG_FILE

def normalize_text(s):
    if not isinstance(s, str):
        return ""
    s = s.lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s

def build_term_variants(term):
    t = normalize_text(term).strip()
    variants = set()
    variants.add(t)
    variants.add(t.replace(' ', '-'))
    variants.add(t.replace('-', ' '))
    if t.endswith('s'):
        variants.add(t[:-1])
    if t.endswith('es'):
        variants.add(t[:-2])
    tokens = [tok for tok in re.split(r'[\s\-_/]+', t) if tok]
    for tok in tokens:
        variants.add(tok)
    return list(variants)

def analyze_text_for_term(text, term_variants, max_contexts=8):
    txt = normalize_text(text)
    occurrences = 0
    contexts = []
    for v in term_variants:
        for m in re.finditer(re.escape(v), txt):
            occurrences += 1
            start = max(0, m.start() - 80)
            end = min(len(txt), m.end() + 80)
            contexts.append(txt[start:end])
            if len(contexts) >= max_contexts:
                break
        if len(contexts) >= max_contexts:
            break
    score = occurrences
    return occurrences, contexts, score

def analyze_page_for_term(soup, term):
    variants = build_term_variants(term)
    title = soup.title.get_text(strip=True) if soup.title else ""
    meta_desc = ""
    meta = soup.find('meta', attrs={'name': 'description'})
    if meta and meta.get('content'):
        meta_desc = meta.get('content', '').strip()
    body_text = soup.get_text(separator=' ', strip=True)
    occ_title, ctx_title, _ = analyze_text_for_term(title, variants, max_contexts=2)
    occ_meta, ctx_meta, _ = analyze_text_for_term(meta_desc, variants, max_contexts=2)
    occ_body, ctx_body, _ = analyze_text_for_term(body_text, variants, max_contexts=8)
    total_occ = occ_title + occ_meta + occ_body
    score = total_occ + (2 if occ_title else 0) + (1 if occ_meta else 0)
    contexts = ctx_title + ctx_meta + ctx_body
    return {
        'Ocorrencias': total_occ,
        'Score': score,
        'Contextos': " | ".join(contexts[:8]),
        'TituloExtraido': title,
        'MetaDescExtraida': meta_desc
    }

def get_headers():
    ua = random.choice(USER_AGENTS)
    return {
        'User-Agent': ua,
        'Accept-Language': 'en-US,en;q=0.8,pt-BR;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

def normalize_onion_url(href, base_url):
    if not href:
        return None
    if href.startswith('//'):
        href = 'http:' + href
    abs_url = urllib.parse.urljoin(base_url, href)
    parsed = urllib.parse.urlparse(abs_url)
    if '.onion' in abs_url and not parsed.scheme:
        abs_url = 'http://' + abs_url
    return abs_url

def fetch_url(url, proxies, timeout=60, retries=2):
    attempt = 0
    while attempt <= retries:
        try:
            headers = get_headers()
            if LOGGER:
                LOGGER.debug(f"Requisição: {url} tentativa={attempt+1} timeout={timeout}")
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            if resp.status_code == 200:
                if LOGGER:
                    LOGGER.debug(f"Resposta 200: {url} tamanho={len(resp.text)}")
                return resp
            if resp.status_code in (429, 503):
                delay = random.uniform(3, 7) * (attempt + 1)
                if LOGGER:
                    LOGGER.warning(f"Resposta {resp.status_code}: {url} aguardando {delay:.1f}s")
                time.sleep(delay)
            else:
                if LOGGER:
                    LOGGER.error(f"Resposta {resp.status_code}: {url}")
                return None
        except requests.exceptions.Timeout:
            delay = random.uniform(2, 4) * (attempt + 1)
            if LOGGER:
                LOGGER.warning(f"Timeout: {url} aguardando {delay:.1f}s")
            time.sleep(delay)
        except requests.exceptions.ConnectionError:
            delay = random.uniform(2, 4) * (attempt + 1)
            if LOGGER:
                LOGGER.warning(f"Conexão falhou: {url} aguardando {delay:.1f}s")
            time.sleep(delay)
        attempt += 1
    if LOGGER:
        LOGGER.error(f"Sem resposta após {retries+1} tentativas: {url}")
    return None
def get_tor_port():
    """Detecta automaticamente a porta do Tor (9150 ou 9050)."""
    ports = [9150, 9050]
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            s.close()
            if result == 0:
                return port
        except:
            pass
    return None

def check_tor_connection(proxies):
    """Verifica se a conexão está passando pelo Tor."""
    try:
        print(colored("[INFO] Verificando conexão com a rede Tor...", "yellow"))
        r = requests.get('https://check.torproject.org/api/ip', proxies=proxies, timeout=30)
        if r.status_code == 200:
            data = r.json()
            if data.get('IsTor', False):
                print(colored(f"[SUCESSO] Conectado ao Tor! IP: {data.get('IP')}", "green"))
                return True
            else:
                print(colored(f"[PERIGO] NÃO conectado ao Tor. IP: {data.get('IP')}", "red", attrs=['bold']))
                return False
    except Exception as e:
        print(colored(f"[ERRO] Falha ao conectar ao Tor: {e}", "red"))
        return False
    return False

def parse_generic(soup, term, base_url):
    """Tenta extrair resultados de qualquer buscador simples."""
    results = []
    parsed_base = urllib.parse.urlparse(base_url)
    base_host = parsed_base.netloc
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        resolved = normalize_onion_url(href, base_url) if href else None
        if resolved and '.onion' in resolved:
            target_host = urllib.parse.urlparse(resolved).netloc
            if target_host and base_host and target_host == base_host:
                continue
                
            title = link.get_text(strip=True)
            if not title:
                title = resolved
                
            # Snippet simples (texto ao redor ou pai)
            snippet = ""
            parent = link.parent
            if parent:
                snippet = parent.get_text(strip=True)[:200]
            
            results.append({
                'Termo Pesquisado': term,
                'Título': title,
                'URL': resolved,
                'Snippet': snippet,
                'Data': pd.Timestamp.now()
            })
    return results

def find_next_page(soup, current_url):
    """Tenta encontrar o link para a próxima página de resultados."""
    link = soup.find('link', rel='next')
    if link and link.get('href'):
        return link.get('href')
    
    a_rel_next = soup.find('a', attrs={'rel': 'next'})
    if a_rel_next and a_rel_next.get('href'):
        return a_rel_next.get('href')
    
    next_regex = re.compile(r'(next|próxima|proxima|seguinte|older|following|more|siguiente|suivant|avançar|avancar|>>|›|»)', re.IGNORECASE)
    
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True).lower()
        if next_regex.search(text):
            return a['href']
        classes = a.get('class') or []
        if any('next' in str(c).lower() for c in classes):
            return a['href']
            
    def _extract_current_page(url, soup_obj):
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        for key in ['page', 'p', 'pg']:
            if key in qs:
                try:
                    return int(qs[key][0])
                except:
                    pass
        indicators = ['active', 'current', 'selected', 'page-current']
        for cls in indicators:
            el = soup_obj.find(class_=cls)
            if el:
                t = el.get_text(strip=True)
                if t.isdigit():
                    try:
                        return int(t)
                    except:
                        pass
        return None
    
    numeric_candidates = []
    for a in soup.find_all('a', href=True):
        t = a.get_text(strip=True)
        if not t:
            continue
        m = re.fullmatch(r'\d+', t)
        if m:
            try:
                n = int(t)
                numeric_candidates.append((n, a['href']))
            except:
                pass
    
    if numeric_candidates:
        current_page = _extract_current_page(current_url, soup)
        numeric_candidates.sort(key=lambda x: x[0])
        if current_page is not None:
            for n, href in numeric_candidates:
                if n > current_page:
                    return href
        else:
            for n, href in numeric_candidates:
                if n > 1:
                    return href
            return numeric_candidates[0][1]
    
    return None

def find_next_page_torch(soup, current_url):
    parsed = urllib.parse.urlparse(current_url)
    qs = urllib.parse.parse_qs(parsed.query)
    def _get_int(d, k, default):
        try:
            return int(d.get(k, [default])[0])
        except:
            return default
    current_top = _get_int(qs, 'TOPDOC', 0)
    current_page = _get_int(qs, '[', 1)  # '[=' vira chave '['
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True).lower()
        if 'omega' in href and ('TOPDOC=' in href or '%5B=' in href):
            if re.search(r'(next|próxima|proxima|>>|›|»)', text, re.IGNORECASE):
                return href
            try:
                hq = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                top = _get_int(hq, 'TOPDOC', -1)
                if top > current_top:
                    return href
            except:
                continue
    next_qs = {k: v[:] for k, v in qs.items()}
    next_qs['TOPDOC'] = [str(current_top + 10 if current_top >= 0 else 10)]
    next_qs['['] = [str(current_page + 1)]
    new_query = urllib.parse.urlencode(next_qs, doseq=True)
    next_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    return next_url

def parse_ahmia(soup, term, base_url):
    results = []
    items = soup.select('li.result') or soup.select('li[class*="result"]') or soup.select('div.result') or soup.select('article.result') or soup.select('#results li')
    if items:
        for item in items:
            link_tag = item.find('a', href=True)
            if not link_tag:
                continue
            resolved_link = normalize_onion_url(link_tag.get('href'), base_url)
            if not resolved_link or '.onion' not in resolved_link:
                continue
            snippet_tag = item.find('p')
            results.append({
                'Termo Pesquisado': term,
                'Motor de Busca': 'Ahmia',
                'Título': link_tag.get_text(strip=True) or resolved_link,
                'URL': resolved_link,
                'Snippet': snippet_tag.get_text(strip=True)[:200] if snippet_tag else "",
                'Data': pd.Timestamp.now()
            })
    else:
        results = parse_generic(soup, term, base_url)
        for r in results:
            r['Motor de Busca'] = 'Ahmia'
    return results

def search_engine(name, engine_config, term, proxies):
    """Realiza a busca em um motor específico com paginação automática."""
    results = []
    
    # URL Inicial
    current_url = engine_config['url'].format(query=urllib.parse.quote_plus(term))
    
    # Limite de segurança para evitar loops infinitos
    MAX_PAGES = 3 
    pages_crawled = 0
    
    print(f"  > Pesquisando '{term}' no {name}...")
    if LOGGER:
        LOGGER.info(f"Iniciando busca termo='{term}' motor='{name}' url='{current_url}'")
    
    while current_url and pages_crawled < MAX_PAGES:
        if pages_crawled > 0:
            print(f"    >> Buscando página {pages_crawled + 1}...")
        if LOGGER:
            LOGGER.info(f"Página {pages_crawled + 1} motor='{name}' url='{current_url}'")
            
        try:
            resp = fetch_url(current_url, proxies, timeout=60, retries=2)
            
            if resp and resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                page_results = []
                
                if name == 'Ahmia':
                    page_results = parse_ahmia(soup, term, current_url)
                else:
                    # Parser Genérico
                    generic_results = parse_generic(soup, term, current_url)
                    # Adiciona o nome do motor
                    for res in generic_results:
                        res['Motor de Busca'] = name
                    page_results.extend(generic_results)
                    
                results.extend(page_results)
                print(colored(f"    -> {len(page_results)} resultados nesta página.", "cyan"))
                if LOGGER:
                    LOGGER.info(f"Resultados coletados motor='{name}' pagina={pages_crawled + 1} qtd={len(page_results)}")
                
                try:
                    visited = set()
                    for r in page_results:
                        url = r.get('URL')
                        if not isinstance(url, str) or '.onion' not in url:
                            continue
                        if url in visited:
                            continue
                        visited.add(url)
                        if LOGGER:
                            LOGGER.debug(f"Analisando termo em url='{url}'")
                        page_resp = fetch_url(url, proxies, timeout=45, retries=1)
                        if page_resp and page_resp.status_code == 200:
                            page_soup = BeautifulSoup(page_resp.text, 'html.parser')
                            analysis = analyze_page_for_term(page_soup, term)
                            r.update(analysis)
                            r['Status'] = '200'
                        else:
                            r['Status'] = str(page_resp.status_code) if page_resp else 'error'
                except Exception as e:
                    if LOGGER:
                        LOGGER.exception("Falha ao analisar páginas da lista")
                
                # Tenta encontrar a próxima página
                if name == 'Torch':
                    next_link = find_next_page_torch(soup, current_url)
                else:
                    next_link = find_next_page(soup, current_url)
                if next_link:
                    # Resolve URL relativa se necessário
                    current_url = urllib.parse.urljoin(current_url, next_link)
                    pages_crawled += 1
                    
                    # Pausa aleatória para simular humano e dar tempo de carregar/estabilizar Tor
                    wait_time = random.uniform(5, 10)
                    print(colored(f"    ... Aguardando {wait_time:.1f}s para próxima página ...", "yellow"))
                    if LOGGER:
                        LOGGER.info(f"Próxima página motor='{name}' aguardando={wait_time:.1f}s next='{current_url}'")
                    time.sleep(wait_time)
                else:
                    if LOGGER:
                        LOGGER.info(f"Sem próxima página motor='{name}'")
                    break # Sem mais páginas
                    
            else:
                print(colored(f"    [X] {name} retornou status {resp.status_code if resp else 'sem resposta'}", "red"))
                if LOGGER:
                    LOGGER.error(f"Falha resposta motor='{name}' status='{resp.status_code if resp else 'none'}'")
                break
                
        except requests.exceptions.Timeout:
            print(colored(f"    [X] Timeout ao conectar com {name}", "red"))
            if LOGGER:
                LOGGER.error(f"Timeout motor='{name}'")
            break
        except requests.exceptions.ConnectionError:
            print(colored(f"    [X] Falha de conexão com {name} (Pode estar offline)", "red"))
            if LOGGER:
                LOGGER.error(f"Conexão falhou motor='{name}'")
            break
        except Exception as e:
            print(colored(f"    [X] Erro inesperado no {name}: {e}", "red"))
            if LOGGER:
                LOGGER.exception(f"Erro inesperado motor='{name}'")
            break
        
    return results

def enrich_results(results, proxies, max_fetch=ENRICH_FETCH_LIMIT):
    visited = set()
    fetched = 0
    for r in results:
        if fetched >= max_fetch:
            break
        url = r.get('URL')
        if not isinstance(url, str) or '.onion' not in url:
            continue
        if url in visited:
            continue
        if LOGGER:
            LOGGER.debug(f"Enriquecendo url='{url}'")
        resp = fetch_url(url, proxies, timeout=45, retries=1)
        visited.add(url)
        fetched += 1
        if resp and resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.title.get_text(strip=True) if soup.title else ""
            meta = soup.find('meta', attrs={'name': 'description'})
            meta_desc = meta.get('content', '').strip() if meta and meta.get('content') else ""
            text_snippet = soup.get_text(separator=' ', strip=True)[:500]
            if not r.get('Título'):
                r['Título'] = title if title else r.get('Título', '')
            if not r.get('Snippet'):
                r['Snippet'] = meta_desc if meta_desc else text_snippet
            r['Status'] = '200'
            if LOGGER:
                LOGGER.debug(f"Enriquecimento OK url='{url}'")
        else:
            r['Status'] = str(resp.status_code) if resp else 'error'
            if LOGGER:
                LOGGER.warning(f"Enriquecimento falhou url='{url}' status='{r['Status']}'")

def main():
    print(colored("=== Darkweb Multi-Engine Search Crawler ===", "magenta", attrs=['bold']))
    init_logger()
    if LOGGER:
        LOGGER.info("Início da varredura")
    
    # 1. Configurar Tor
    tor_port = get_tor_port()
    if not tor_port:
        print(colored("\n[CRÍTICO] O Tor não foi detectado (portas 9150/9050 fechadas).", "red"))
        if LOGGER:
            LOGGER.error("Tor não detectado")
        
        if sys.platform.startswith('linux'):
            print(colored(">>> No Kali Linux, execute: sudo service tor start", "yellow", attrs=['bold']))
        else:
            print(colored(">>> Abra o Tor Browser e deixe-o aberto antes de rodar este script.", "yellow", attrs=['bold']))
        if LOGGER:
            LOGGER.info("Encerrando por ausência de Tor")
        return

    print(colored(f"[INFO] Tor detectado na porta {tor_port}.", "green"))
    tor_proxy = f'socks5h://127.0.0.1:{tor_port}'
    proxies = {'http': tor_proxy, 'https': tor_proxy}
    if LOGGER:
        LOGGER.info(f"Tor detectado porta={tor_port}")

    if not check_tor_connection(proxies):
        if LOGGER:
            LOGGER.error("Verificação Tor falhou")
        return

    # 2. Obter Termo de Pesquisa (Modo Input Direto)
    if len(sys.argv) > 1:
        # Se passado via linha de comando (ex: pelo Dashboard ou terminal)
        termo_input = " ".join(sys.argv[1:])
        terms = [termo_input]
        print(colored(f"\n[INFO] Buscando por: {termo_input}", "cyan"))
        if LOGGER:
            LOGGER.info(f"Termo recebido via argumento='{termo_input}'")
    else:
        # Modo Interativo
        print(colored("\n--- MODO DE PESQUISA MANUAL ---", "cyan", attrs=['bold']))
        termo_input = input(colored("Digite o termo que deseja procurar na Darkweb: ", "yellow")).strip()
        
        if not termo_input:
            print(colored("[!] Nenhum termo inserido. Encerrando.", "red"))
            if LOGGER:
                LOGGER.info("Nenhum termo inserido")
            return
        terms = [termo_input]
        if LOGGER:
            LOGGER.info(f"Termo inserido='{termo_input}'")

    all_findings = []

    # 3. Loop de Busca
    for term in terms:
        print(colored(f"\n[*] Iniciando busca por: {term}", "yellow"))
        if LOGGER:
            LOGGER.info(f"Início busca termo='{term}'")
        
        for engine_name, config in SEARCH_ENGINES.items():
            findings = search_engine(engine_name, config, str(term), proxies)
            all_findings.extend(findings)
            # Pausa para não sobrecarregar circuitos e evitar bloqueios
            time.sleep(random.uniform(2, 5)) 
            if LOGGER:
                LOGGER.info(f"Motor concluído='{engine_name}' acumulado={len(all_findings)}")

    # 4. Relatório
    if all_findings:
        output_file = 'resultados_busca_darkweb.xlsx'
        try:
            enrich_results(all_findings, proxies, ENRICH_FETCH_LIMIT)
        except Exception as e:
            print(colored(f"[AVISO] Enriquecimento falhou: {e}", "yellow"))
            if LOGGER:
                LOGGER.exception("Falha no enriquecimento")
        new_results = pd.DataFrame(all_findings)
        
        # Carregar resultados existentes se houver
        if os.path.exists(output_file):
            try:
                existing_df = pd.read_excel(output_file)
                print(colored(f"[INFO] Mesclando com {len(existing_df)} resultados anteriores...", "cyan"))
                df_results = pd.concat([existing_df, new_results], ignore_index=True)
                if LOGGER:
                    LOGGER.info(f"Mesclagem com resultados anteriores qtd={len(existing_df)}")
            except Exception as e:
                print(colored(f"[AVISO] Não foi possível ler o arquivo existente (será sobrescrito): {e}", "yellow"))
                df_results = new_results
                if LOGGER:
                    LOGGER.warning("Falha leitura arquivo existente, sobrescrevendo")
        else:
            df_results = new_results
        
        # Limpeza e Deduplicação (mantém o mais recente se houver duplicata exata de URL+Termo, ou só URL?)
        # Vamos dedublicar por URL para não ter o mesmo link repetido várias vezes
        df_results.drop_duplicates(subset=['URL'], keep='last', inplace=True)
        
        try:
            df_results.to_excel(output_file, index=False)
            print(colored(f"\n[SUCESSO] Relatório atualizado em: {output_file}", "green", attrs=['bold']))
            print(f"Total de Links Únicos (Acumulado): {len(df_results)}")
            print(f"Novos Links nesta rodada: {len(new_results)}")
            if LOGGER:
                LOGGER.info(f"Relatório salvo='{output_file}' total={len(df_results)} novos={len(new_results)}")
        except PermissionError:
            print(colored(f"\n[ERRO CRÍTICO] Permissão negada ao salvar '{output_file}'.", "red", attrs=['bold']))
            print(colored(">>> FECHE o arquivo Excel se estiver aberto e tente novamente.", "yellow"))
            if LOGGER:
                LOGGER.error("Permissão negada ao salvar relatório")
        except Exception as e:
            print(colored(f"\n[ERRO] Falha ao salvar o relatório: {e}", "red"))
            if LOGGER:
                LOGGER.exception("Falha ao salvar relatório")
    else:
        print(colored("\n[INFO] Nenhum resultado novo encontrado nos motores consultados.", "yellow"))
        if LOGGER:
            LOGGER.info("Nenhum resultado novo")
    if LOGGER:
        LOGGER.info("Fim da varredura")

if __name__ == "__main__":
    main()
