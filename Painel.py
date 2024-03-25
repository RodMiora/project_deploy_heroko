import streamlit as st
import streamlit_authenticator as stauth
import yaml
import plotly.express as px
import pandas as pd
from supabase import create_client, Client
from config import SUBABASE_URL, SUBABASE_API_KEY
from streamlit_option_menu import option_menu 

# Importando Banco de Dados do SupaBase através de uma variável de ambiente permanente
supabase: Client = create_client(SUBABASE_URL, SUBABASE_API_KEY)


# Função para configurar o título da página
def set_page_title(title):
    st.session_state['Bem Vindo'] = title
    st.markdown(f'<h1 style="font-weight:bold;">{title}</h1>', unsafe_allow_html=True)


# Configurando a página
st.set_page_config(page_title="Sua Sala", page_icon=":bar_chart:", layout="wide")


# Carregando o arquivo de configuração YAML
try:
    with open('C:/Users/a/Desktop/projeto pagina autenticação/project/config.yaml') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    print("O arquivo YAML não foi encontrado.")
    config = None


# Verificando se o arquivo de configuração foi carregado corretamente
if config is not None:
    credentials = config['credentials']
else:
    print("Falha ao carregar o arquivo YAML.")


# Inicializando o objeto de autenticação com a classe correta
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Processo de login
name, authentication_status, username = authenticator.login(
    fields=['username', 'password'],
)

# Verificando o status da autenticação e respondendo de acordo
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.success(f'Bem-vindo(a) {name}!')
    # Crie uma barra lateral para navegação
    with st.sidebar:
        selected = option_menu(
            menu_title="Opções",
            options=["Painel"],
            icons=["clipboard-data"],
            menu_icon="cast",
            default_index=0,
        )
    
    if selected == "Painel":
        st.title(f"Você Selecionou {selected}")

    

    # Página do Dashboard
    if selected == 'Painel':
        # Carregar dados para o dashboard
        uploaded_file = st.file_uploader("Carregar banco de dados", type=["csv", "xlsx"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            # Exibindo todos os gráficos
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Gráfico de Linhas')
                fig_line = px.line(df)
                st.plotly_chart(fig_line)
            with col2:
                st.subheader('Gráfico de Barras')
                fig_bar = px.bar(df)
                st.plotly_chart(fig_bar)
            col3, col4 = st.columns(2)
            with col3:
                st.subheader('Histograma')
                fig_hist = px.histogram(df)
                st.plotly_chart(fig_hist)
            with col4:
                st.subheader('Gráfico de Pontos')
                fig_scatter = px.scatter(df)
                st.plotly_chart(fig_scatter)
    
   
elif authentication_status == False:
    st.error('Nome de usuário/senha incorreto')
elif authentication_status == None:
    st.warning('Por favor, insira seu nome de usuário e senha')

