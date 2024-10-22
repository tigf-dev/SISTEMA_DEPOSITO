import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# --- Configuração da API Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds", 
    "https://www.googleapis.com/auth/spreadsheets"
]

# Credenciais do Google em formato de dicionário
google_credentials = {
    "type": "service_account",
  "project_id": "compact-circlet-429712-t7",
  "private_key_id": "3bf7a88747f1e33d142f12aa75ec66887a4ee0ac",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDJoy4gN9ZMkVjq\nn4ZgxLtn5ObA170flNsdbaKAPpyQi7KfishHK0qk/nHO0nlCMrrtJ7dJ2G+wFKSR\n+LqBS3LCLfl+OwpnDLBoaTGRvYe3bMkkL7phg1z+vmoYZCEQfCsrYi4a4qAXTbKB\nPguN87M9fV7Ot5sp9Bu0uXjF+6yDJ87xg2NGJcBN9RprWPFAUL1rIxMO0alFgNn6\ns+us5koYVF/h0pWOVOrk5ONoWSG2BAO2d/460sp0VIazDJqHDwDbOZD0KMYcS+h/\nZBWPUm3wmDzDYYLLnYl2EQbal9bLwQKhCWDqpPzkK9jsKbetnSQaEdp9336n7hFm\nQYNBcAdnAgMBAAECggEAFvKRxMvmASfHgUgvcGLjWyMTWd4ToXz85N/9zu+RPOgR\nJ5QRT/wuzhFBHYMZlr2URXowI2DU8SqgQhaXDzDpegzmaIXKnMi2aOOT5xy1Tdw9\nFfeyk/dxxXIhO+5lTu16skDFs3yYMJ7AknHfucOC4hwbBpahu4gTASHci1elnfVd\nooRzoIOK+O9bN3EaugsRdwQmTPALzaZz3HlDPWZh0OPUwplKDjRk/9b3QZi/R+aU\nk21Fr84Xh8QqO9rXpmGWXXJ5ySZNfyjMvB1qBW2esS/WZ1gKf4J3nr6AddRcDyMx\n/UQwaMmC/AlkUsReppwZAgnh1TenGaM36EXxSSh0IQKBgQDkIkn/QvtZVZXTft0H\nz5FKlmCDy1g+mK7axBnX1m+bnyZ3uYCL7wPbquiAgHNLLVIfTVCGAXmpOU2Xnaov\nqa3pE17d2eD4231DXimneFPTuSPfYle7uxm2M/G6p4e70Garxq1PFh6IVoyYJPjb\nDG2p4YBBRJJmrpbVHWmPwlld4QKBgQDiRFltLYgoG6DHHGNmN7FF1JWenseHNUfh\nN6CXcdc+G1oGNb05TCuWsT5EPGJmvPCM1bCEu3Det4uPGQ3uOraVa3Yop88ztZlc\nn/Y1OLq9v3E4mHAVXww4rR7uJHKH+ba7rcjnFNUhzFW8yFWFmo1zUTvYpli8SV8l\nPJzLAjq+RwKBgCEY6GtkKFsZk5cPfLm5X3bWwkHcqnzKYfPTJ3ys25xURpxwCTpD\n/udLsFeUSyXI+XUZHmmSpTfr3Fn2wc4Qa+64pLbC+WShU1cGvjxRtLeu0ImEFv5h\ncqWAe718uLCC16JsPJCQwPU+uT8JfiEpeG+BC75sWGEVS0S386yroZOBAoGBAIBH\nJbfq/21VtIINyyCxZFRloGmsNQynnVfG9MnHZbM1SIWKw/uO/otRcy62WUdLyMjf\ngVLO/b+WqY14M9ii+s6dfQCxmpwDUa4cljY4Mk7PEX53ldvX5hLfu1Bh43jJjtq6\nPNMdkXO258i+fxXeuGDvZhF+xYIByupOgcnqOqmTAoGAUbbpfRTLnmzSHbGg6RGH\nDMV8qCDx8xNajW1Xb1mEvaR+LvOtDiX0NIjs44wJjSHprhEGGOfO8yanVQCx4y8g\nfiUcU2O0owp0z9fgK+MQtu3vGdGUO6fpPOwezaQrCsnbAz72Mc4nrTNq93y9l1Hx\ntSYy4gTeQq6G7wXxqQXT+g8=\n-----END PRIVATE KEY-----\n",
  "client_email": "automa-o-preco-e-custo@compact-circlet-429712-t7.iam.gserviceaccount.com",
  "client_id": "104336409081084239932",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/automa-o-preco-e-custo%40compact-circlet-429712-t7.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Converter de dicionário para JSON
creds_dict = json.dumps(google_credentials)

# Carregar as credenciais
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_dict), scope)
client = gspread.authorize(creds)

# --- Carrega os dados da planilha ---
spreadsheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1AZ2K-U1i-zyEeqsk42MQzBbrxxNhIPEEhFQ000kouqI/edit?gid=0#gid=0"
)
worksheet = spreadsheet.worksheet("COLMEIA")
data = worksheet.get_all_records()

# Criação do DataFrame
df = pd.DataFrame(data)

# --- Exibir a planilha completa ---
st.markdown("<h1 style='text-align: center;'>Sistema de Estoque - Mapeamento de Colmeias</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Visualização Completa da Planilha</h2>", unsafe_allow_html=True)

# Usar use_container_width=True para ocupar toda a largura disponível
st.dataframe(df, use_container_width=True)

# --- Tabela estilo Batalha Naval ---
st.markdown("<h2 style='text-align: center;'>Visualização Estilo Batalha Naval</h2>", unsafe_allow_html=True)

# Criar uma tabela para a visualização estilo Batalha Naval
colmeias = df['Localização colmeia'].unique()  # Colunas são as localizações das colmeias
espacos = df['Localização espaços'].unique()  # Linhas são os espaços

# Criação da tabela de batalha naval
tabela_batalha = pd.DataFrame(index=espacos, columns=colmeias)

# Preencher a tabela com HTML de tooltip ou "Vazio"
for _, row in df.iterrows():
    col = row['Localização colmeia']
    row_idx = row['Localização espaços']
    if col in tabela_batalha.columns and row_idx in tabela_batalha.index:
        if row['Descrição'] and row['Quantidade'] > 0:
            descricao = f"{row['Descrição']} ({row['Quantidade']})"
            tooltip_html = f"""
                <div class="tooltip">
                    <span class="tooltiptext">{descricao}</span>
                    Peça Oculta
                </div>
            """
            # Se a célula estiver vazia ou contiver "Vazio", adicione o tooltip_html
            if pd.isna(tabela_batalha.at[row_idx, col]) or tabela_batalha.at[row_idx, col] == "Vazio":
                tabela_batalha.at[row_idx, col] = tooltip_html
            else:
                # Concatenar se já houver um valor
                tabela_batalha.at[row_idx, col] += f"<br>{tooltip_html}"
        else:
            tabela_batalha.at[row_idx, col] = "Vazio"

# Substituir "\n" por "" (nada) e manter "Vazio" como está
tabela_batalha.replace("\n", "", regex=True, inplace=True)

# --- Estilo CSS para o tooltip e centralização ---
st.markdown("""
    <style>
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
        border-bottom: 1px dotted black;
        color: transparent; /* Torna o texto "Peça Oculta" invisível */
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 160px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;  /* Posição acima do texto */
        left: 50%;
        margin-left: -80px;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }

    /* Centralizar a tabela */
    .tabela-centralizada {
        display: flex;
        justify-content: center;
    }

    /* Centralizar o texto nas células da tabela */
    table {
        margin: 0 auto; /* Centraliza a tabela na página */
        border-collapse: collapse; /* Remove espaços entre as células */
    }
    th, td {
        text-align: center; /* Centraliza o texto das células */
        padding: 10px; /* Adiciona espaço interno nas células */
        border: 1px solid black; /* Adiciona bordas às células */
    }
    </style>
""", unsafe_allow_html=True)

# Exibir a tabela de batalha naval com HTML seguro, dentro de um container centralizado
st.markdown(
    f'<div class="tabela-centralizada">{tabela_batalha.to_html(escape=False)}</div>',
    unsafe_allow_html=True
)
