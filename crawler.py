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
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            if resp.status_code == 200:
                return resp
            if resp.status_code in (429, 503):
                delay = random.uniform(3, 7) * (attempt + 1)
                time.sleep(delay)
            else:
                return None
        except requests.exceptions.Timeout:
            delay = random.uniform(2, 4) * (attempt + 1)
            time.sleep(delay)
        except requests.exceptions.ConnectionError:
            delay = random.uniform(2, 4) * (attempt + 1)
            time.sleep(delay)
        attempt += 1
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
    # Procura todos os links
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        resolved = normalize_onion_url(href, base_url) if href else None
        if resolved and '.onion' in resolved:
            # Filtra links internos ou irrelevantes
            if 'search' in resolved or '?' in resolved and len(resolved) < 20:
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
    
    next_texts = ['next', 'next >', '>>', 'more', 'older', 'following', 'próxima', 'proxima']
    
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True).lower()
        if text in next_texts:
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

def search_engine(name, engine_config, term, proxies):
    """Realiza a busca em um motor específico com paginação automática."""
    results = []
    
    # URL Inicial
    current_url = engine_config['url'].format(query=urllib.parse.quote_plus(term))
    
    # Limite de segurança para evitar loops infinitos
    MAX_PAGES = 3 
    pages_crawled = 0
    
    print(f"  > Pesquisando '{term}' no {name}...")
    
    while current_url and pages_crawled < MAX_PAGES:
        if pages_crawled > 0:
            print(f"    >> Buscando página {pages_crawled + 1}...")
            
        try:
            resp = fetch_url(current_url, proxies, timeout=60, retries=2)
            
            if resp and resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                page_results = []
                
                if engine_config['selector'] == 'li.result':
                    # Parser específico do Ahmia
                    items = soup.select('li.result')
                    for item in items:
                        link_tag = item.find('a')
                        snippet_tag = item.find('p')
                        if link_tag:
                            resolved_link = normalize_onion_url(link_tag.get('href'), current_url)
                            page_results.append({
                                'Termo Pesquisado': term,
                                'Motor de Busca': name,
                                'Título': link_tag.get_text(strip=True),
                                'URL': resolved_link,
                                'Snippet': snippet_tag.get_text(strip=True) if snippet_tag else "",
                                'Data': pd.Timestamp.now()
                            })
                else:
                    # Parser Genérico
                    generic_results = parse_generic(soup, term, current_url)
                    # Adiciona o nome do motor
                    for res in generic_results:
                        res['Motor de Busca'] = name
                    page_results.extend(generic_results)
                    
                results.extend(page_results)
                print(colored(f"    -> {len(page_results)} resultados nesta página.", "cyan"))
                
                # Tenta encontrar a próxima página
                next_link = find_next_page(soup, current_url)
                if next_link:
                    # Resolve URL relativa se necessário
                    current_url = urllib.parse.urljoin(current_url, next_link)
                    pages_crawled += 1
                    
                    # Pausa aleatória para simular humano e dar tempo de carregar/estabilizar Tor
                    wait_time = random.uniform(5, 10)
                    print(colored(f"    ... Aguardando {wait_time:.1f}s para próxima página ...", "yellow"))
                    time.sleep(wait_time)
                else:
                    break # Sem mais páginas
                    
            else:
                print(colored(f"    [X] {name} retornou status {resp.status_code if resp else 'sem resposta'}", "red"))
                break
                
        except requests.exceptions.Timeout:
            print(colored(f"    [X] Timeout ao conectar com {name}", "red"))
            break
        except requests.exceptions.ConnectionError:
            print(colored(f"    [X] Falha de conexão com {name} (Pode estar offline)", "red"))
            break
        except Exception as e:
            print(colored(f"    [X] Erro inesperado no {name}: {e}", "red"))
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
        else:
            r['Status'] = str(resp.status_code) if resp else 'error'

def main():
    print(colored("=== Darkweb Multi-Engine Search Crawler ===", "magenta", attrs=['bold']))
    
    # 1. Configurar Tor
    tor_port = get_tor_port()
    if not tor_port:
        print(colored("\n[CRÍTICO] O Tor não foi detectado (portas 9150/9050 fechadas).", "red"))
        
        if sys.platform.startswith('linux'):
            print(colored(">>> No Kali Linux, execute: sudo service tor start", "yellow", attrs=['bold']))
        else:
            print(colored(">>> Abra o Tor Browser e deixe-o aberto antes de rodar este script.", "yellow", attrs=['bold']))
        return

    print(colored(f"[INFO] Tor detectado na porta {tor_port}.", "green"))
    tor_proxy = f'socks5h://127.0.0.1:{tor_port}'
    proxies = {'http': tor_proxy, 'https': tor_proxy}

    if not check_tor_connection(proxies):
        return

    # 2. Obter Termo de Pesquisa (Modo Input Direto)
    if len(sys.argv) > 1:
        # Se passado via linha de comando (ex: pelo Dashboard ou terminal)
        termo_input = " ".join(sys.argv[1:])
        terms = [termo_input]
        print(colored(f"\n[INFO] Buscando por: {termo_input}", "cyan"))
    else:
        # Modo Interativo
        print(colored("\n--- MODO DE PESQUISA MANUAL ---", "cyan", attrs=['bold']))
        termo_input = input(colored("Digite o termo que deseja procurar na Darkweb: ", "yellow")).strip()
        
        if not termo_input:
            print(colored("[!] Nenhum termo inserido. Encerrando.", "red"))
            return
        terms = [termo_input]

    all_findings = []

    # 3. Loop de Busca
    for term in terms:
        print(colored(f"\n[*] Iniciando busca por: {term}", "yellow"))
        
        for engine_name, config in SEARCH_ENGINES.items():
            findings = search_engine(engine_name, config, str(term), proxies)
            all_findings.extend(findings)
            # Pausa para não sobrecarregar circuitos e evitar bloqueios
            time.sleep(random.uniform(2, 5)) 

    # 4. Relatório
    if all_findings:
        output_file = 'resultados_busca_darkweb.xlsx'
        try:
            enrich_results(all_findings, proxies, ENRICH_FETCH_LIMIT)
        except Exception as e:
            print(colored(f"[AVISO] Enriquecimento falhou: {e}", "yellow"))
        new_results = pd.DataFrame(all_findings)
        
        # Carregar resultados existentes se houver
        if os.path.exists(output_file):
            try:
                existing_df = pd.read_excel(output_file)
                print(colored(f"[INFO] Mesclando com {len(existing_df)} resultados anteriores...", "cyan"))
                df_results = pd.concat([existing_df, new_results], ignore_index=True)
            except Exception as e:
                print(colored(f"[AVISO] Não foi possível ler o arquivo existente (será sobrescrito): {e}", "yellow"))
                df_results = new_results
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
        except PermissionError:
            print(colored(f"\n[ERRO CRÍTICO] Permissão negada ao salvar '{output_file}'.", "red", attrs=['bold']))
            print(colored(">>> FECHE o arquivo Excel se estiver aberto e tente novamente.", "yellow"))
        except Exception as e:
            print(colored(f"\n[ERRO] Falha ao salvar o relatório: {e}", "red"))
    else:
        print(colored("\n[INFO] Nenhum resultado novo encontrado nos motores consultados.", "yellow"))

if __name__ == "__main__":
    main()
