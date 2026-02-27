import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Portal do Cliente - Saúde", page_icon="🏥")

st.title("🏥 Acompanhamento de Contrato")
st.subheader("Consulte o status do seu plano de saúde")

# Link da sua planilha (Versão de exportação CSV para facilitar o Pandas)
# Substitua 'ID_DA_SUA_PLANILHA' pelo código longo que aparece na URL da sua planilha
SHEET_ID = '1pGnxZ2GCc5Bw4rBbjujUKt62IVBcrviqjxzGXDr3Ggg'
URL = f'https://docs.google.com/spreadsheets/d/1pGnxZ2GCc5Bw4rBbjujUKt62IVBcrviqjxzGXDr3Ggg/edit?usp=sharing'

# Função para carregar dados
def carregar_dados():
    try:
        return pd.read_csv(URL)
    except Exception as e:
        st.error("Não foi possível conectar à planilha. Verifique se ela está compartilhada como 'Qualquer pessoa com o link'.")
        return None

# Interface de Login
with st.container():
    cpf_input = st.text_input("Digite seu CPF (com pontos e traço):")
    nasc_input = st.text_input("Digite sua Data de Nascimento (DD/MM/AAAA):")
    
    if st.button("Consultar Status"):
        df = carregar_dados()
        
        # Filtra o cliente na planilha
        cliente = df[(df['cpf'] == cpf_input) & (df['nascimento'] == nasc_input)]
        
        if not cliente.empty:
            nome = cliente['nome'].values[0]
            status = cliente['status'].values[0]
            
            st.success(f"Olá, **{nome}**!")
            
            # Estilização baseada no status
            if "Recusado" in status:
                st.error(f"Status Atual: {status}")
            elif "Agendado" in status:
                st.info(f"Status Atual: {status}")
            else:
                st.warning(f"Status Atual: {status}")
        else:
            st.error("Usuário não encontrado. Verifique os dados digitados.")

            

st.markdown("---")
st.caption("Dúvidas? Entre em contato com nosso suporte via WhatsApp.")