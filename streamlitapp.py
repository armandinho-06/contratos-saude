import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Portal do Cliente - Saúde", page_icon="🏥")

# SEU ID REAL DA PLANILHA
SHEET_ID = '1pGnxZ2GCc5Bw4rBbjujUKt62IVBcrviqjxzGXDr3Ggg'
# O link abaixo é o segredo para transformar a planilha em dados que o Python entende
URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'
def carregar_dados():
    try:
        df = pd.read_csv(URL, dtype=str)
        # Remove espaços em branco antes ou depois de QUALQUER texto na planilha
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
        return None

st.title("🏥 Acompanhamento de Contrato")
st.subheader("Consulte o status do seu plano de saúde")

# Interface de Login
cpf_input = st.text_input("Digite seu CPF (ex: 123.456.789-00):")
nasc_input = st.text_input("Digite sua Data de Nascimento (DD/MM/AAAA):")

if st.button("Consultar Status"):
    df = carregar_dados()
    
    if df is not None:
        # .strip() remove espaços que o cliente pode ter digitado sem querer
        cpf_limpo = cpf_input.strip()
        nasc_limpa = nasc_input.strip()
        
        cliente = df[(df['cpf'] == cpf_limpo) & (df['nascimento'] == nasc_limpa)]
        # ... resto do código
    
    if df is not None:
        # O filtro agora procura exatamente o que o cliente digitou
        cliente = df[(df['cpf'] == cpf_input) & (df['nascimento'] == nasc_input)]
        
        if not cliente.empty:
            nome = cliente['nome'].values[0]
            status = cliente['status'].values[0]
            st.success(f"Olá, **{nome}**!")
            st.info(f"O status atual do seu contrato é: **{status}**")
        else:
            st.error("Dados não encontrados. Verifique o CPF e a data.")