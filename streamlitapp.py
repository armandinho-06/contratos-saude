import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Portal do Cliente - Saúde", page_icon="🏥")

# SEU ID REAL DA PLANILHA
SHEET_ID = '1pGnxZ2GCc5Bw4rBbjujUKt62IVBcrviqjxzGXDr3Ggg'
URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'

def carregar_dados():
    try:
        df = pd.read_csv(URL, dtype=str)
        # Limpa espaços extras de todas as células
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        # Cria uma coluna secreta apenas com números para o CPF facilitar a busca
        df['cpf_busca'] = df['cpf'].str.replace(r'\D', '', regex=True)
        return df
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
        return None

st.title("🏥 Acompanhamento de Contrato")
st.subheader("Consulte o status do seu plano de saúde")

# Interface de Login
cpf_input = st.text_input("Digite seu CPF (apenas números ou com pontos):")
nasc_input = st.text_input("Digite sua Data de Nascimento (DD/MM/AAAA):")

if st.button("Consultar Status"):
    if not cpf_input or not nasc_input:
        st.warning("Por favor, preencha o CPF e a Data de Nascimento.")
    else:
        df = carregar_dados()
        
        if df is not None:
            # Prepara a busca: ignora pontos/traços que o cliente digitar
            cpf_cliente_so_numeros = "".join(filter(str.isdigit, cpf_input))
            nasc_cliente = nasc_input.strip()
            
            # Busca na planilha
            cliente = df[(df['cpf_busca'] == cpf_cliente_so_numeros) & (df['nascimento'] == nasc_cliente)]
            
            if not cliente.empty:
                nome = cliente['nome'].values[0]
                status = cliente['status'].values[0]
                
                st.markdown(f"### Olá, **{nome}**!")
                
                # Estilização visual por Status
                if "Análise" in status or "Aguardando" in status:
                    st.warning(f"🟡 **Status:** {status}")
                elif "Agendado" in status:
                    st.success(f"🟢 **Status:** {status}")
                elif "Recusado" in status:
                    st.error(f"🔴 **Status:** {status}")
                else:
                    st.info(f"🔵 **Status:** {status}")
            else:
                st.error("Dados não encontrados. Verifique se o CPF e a Data estão corretos.")