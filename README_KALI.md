# Darkweb Crawler - Guia para Kali Linux

Este projeto foi adaptado para rodar nativamente no Kali Linux.

## Pré-requisitos
O script `setup_kali.sh` cuidará de quase tudo, mas você precisa ter privilégios `sudo`.

## Instalação Rápida

1. Abra o terminal na pasta do projeto.
2. Dê permissão de execução e rode o script de instalação:
   ```bash
   chmod +x setup_kali.sh
   ./setup_kali.sh
   ```

Este script irá:
- Instalar o serviço `tor` e pacotes Python necessários.
- Iniciar o serviço Tor (porta 9050).
- Criar um ambiente virtual (`venv`) para isolar as bibliotecas.
- Instalar as dependências do `requirements.txt`.

## Como Usar

Sempre que for usar, você precisa ativar o ambiente virtual:

1. **Ative o ambiente:**
   ```bash
   source venv/bin/activate
   ```

2. **Execute o Crawler:**
   ```bash
   python crawler.py
   ```

3. **Verifique os resultados:**
   O arquivo `resultados_busca_darkweb.xlsx` será gerado na mesma pasta.

## Solução de Problemas

- **Erro "Tor não detectado":**
  Verifique se o serviço caiu. Reinicie com:
  ```bash
  sudo service tor restart
  ```

- **Erro de Permissão:**
  Certifique-se de usar `sudo` apenas para instalar pacotes do sistema (`apt`), não para rodar o script python (o venv cuida disso).
