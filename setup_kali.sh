#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Configuração Darkweb Crawler para Kali Linux ===${NC}"

# 1. Instalar pacotes do sistema
echo -e "\n${YELLOW}[*] Atualizando lista de pacotes e instalando Tor/Python-venv...${NC}"
sudo apt update
sudo apt install -y tor python3-pip python3-venv

# 2. Configurar Serviço Tor
echo -e "\n${YELLOW}[*] Iniciando serviço Tor...${NC}"
sudo service tor start

# Verificar se iniciou
if systemctl is-active --quiet tor; then
    echo -e "${GREEN}[OK] Serviço Tor está rodando.${NC}"
else
    echo -e "${RED}[ERRO] Falha ao iniciar o Tor. Tente 'sudo service tor start' manualmente.${NC}"
fi

# 3. Configurar Ambiente Virtual Python
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}[*] Criando ambiente virtual (venv)...${NC}"
    python3 -m venv venv
else
    echo -e "\n${YELLOW}[*] Ambiente virtual já existe.${NC}"
fi

# 4. Instalar Dependências
echo -e "\n${YELLOW}[*] Instalando bibliotecas Python...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Finalização
echo -e "\n${GREEN}=== Instalação Concluída! ===${NC}"
echo -e "Para usar o projeto (Recomendado via Dashboard):"
echo -e "1. Ative o ambiente: ${YELLOW}source venv/bin/activate${NC}"
echo -e "2. Inicie o Dashboard: ${YELLOW}python -m streamlit run dashboard.py${NC}"
echo -e "\nOu execute apenas o crawler via terminal:"
echo -e "${YELLOW}python3 crawler.py${NC}"
