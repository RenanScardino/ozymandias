import requests
from termcolor import colored
import sys
import os
import socket

# Configuração Tor
TOR_PROXY = 'socks5h://127.0.0.1:9150'

ENGINES = {
    'Ahmia': 'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q=test',
    'Torch_V1': 'http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P=test',
    'Torch_V2': 'http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search?q=test',
    'Haystak': 'http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/?q=test',
    'OnionLand': 'http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search?q=test'
}

def get_tor_port():
    ports = [9150, 9050]
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            result = s.connect_ex(('127.0.0.1', port))
            s.close()
            if result == 0:
                print(colored(f"[INFO] Serviço Tor detectado na porta {port}", "green"))
                return port
        except:
            pass
    return None

def probe():
    print("Iniciando sondagem de motores de busca (Método SOCKS5h)...")
    
    tor_port = get_tor_port()
    if not tor_port:
        print(colored("[CRÍTICO] Não foi possível detectar o serviço Tor (portas 9150 ou 9050 fechadas).", "red"))
        print(colored("Por favor, abra o Tor Browser e aguarde ele conectar.", "yellow"))
        return

    tor_proxy = f'socks5h://127.0.0.1:{tor_port}'
    
    if not os.path.exists('debug_html'):
        os.makedirs('debug_html')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
    
    proxies = {
        'http': tor_proxy,
        'https': tor_proxy
    }

    for name, url in ENGINES.items():
        print(f"Testando {name}...")
        try:
            # Timeout aumentado para 60s pois Tor pode ser lento
            r = requests.get(url, headers=headers, proxies=proxies, timeout=60)
            if r.status_code == 200:
                print(colored(f"  [OK] {name} respondeu. Salvando HTML...", "green"))
                with open(f'debug_html/{name}.html', 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(r.text)
            else:
                print(colored(f"  [FALHA] {name} retornou status {r.status_code}", "red"))
        except Exception as e:
            print(colored(f"  [ERRO] {name} inacessível: {e}", "red"))

if __name__ == "__main__":
    probe()
