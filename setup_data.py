import pandas as pd
import os

# Criar arquivo de termos (Excel)
df_termos = pd.DataFrame({
    'Termos': ['bitcoin', 'database', 'leak', 'passport']
})
df_termos.to_excel('termos.xlsx', index=False)
print("Arquivo 'termos.xlsx' criado com sucesso.")

# Criar arquivo de URLs (Texto) - Exemplo com Ahmia e um link dummy
urls = [
    "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q=test", # Ahmia Search (exemplo)
    "https://www.facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion/" # Facebook Onion (exemplo seguro)
]

with open('urls.txt', 'w') as f:
    for url in urls:
        f.write(url + '\n')

print("Arquivo 'urls.txt' criado com sucesso.")
