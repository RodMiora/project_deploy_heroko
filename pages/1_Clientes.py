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
            options=["Clientes"],
            icons=["card-checklist"],
            menu_icon="cast",
            default_index=0,
        )
    
    
    if selected == "Clientes":
        st.title(f"Você Selecionou {selected}")
    

    
    # Página de Vendas
    if selected == 'Vendas':
        # Buscando dados da tabela 'vendas' do Supabase que foram inseridos pelo usuário atual
        data = supabase.table('vendas').select('*').filter('usuario', 'eq', username).execute()
        # Convertendo para DataFrame do Pandas e exibindo na página
        df_vendas = pd.DataFrame(data.data)
        st.write(df_vendas)
        # Adicionando um formulário para adicionar novas vendas
        with st.form(key='add_venda'):
            st.header('Adicionar nova venda')
            # Substitua 'coluna1', 'coluna2', etc. pelos nomes reais das colunas
            for col in df_vendas.columns:
                if col != 'id' and col != 'usuario':  # Não permitir a edição do 'id' ou 'usuario'
                    globals()[col] = st.text_input(f'{col}')
            submit_button = st.form_submit_button(label='Adicionar venda')
        # Se o botão for pressionado, adicione a nova venda ao banco de dados
        if submit_button:
            new_venda = {col: globals()[col] for col in df_vendas.columns if col != 'id' and col != 'usuario'}
            new_venda['usuario'] = username  # Adiciona o usuário atual como o inseridor
            supabase.table('vendas').insert(new_venda).execute()

    # Página de Clientes
    elif selected == 'Clientes':
        # Buscando dados da tabela 'clientes' do Supabase que foram inseridos pelo usuário atual
        data = supabase.table('clientes').select('*').filter('usuario', 'eq', username).execute()
        # Convertendo para DataFrame do Pandas e exibindo na página
        df_clientes = pd.DataFrame(data.data)
        st.write(df_clientes)
        # Adicionando um formulário para adicionar novos clientes
        with st.form(key='add_cliente'):
            st.header('Adicionar Cliente')
            # Substitua 'coluna1', 'coluna2', etc. pelos nomes reais das colunas
            for col in df_clientes.columns:
                if col != 'id' and col != 'usuario':  # Não permitir a edição do 'id' ou 'usuario'
                    globals()[col] = st.text_input(f'{col}')
            submit_button = st.form_submit_button(label='Adicionar cliente')
        # Se o botão for pressionado, adicione a novo cliente ao banco de dados
        if submit_button:
            new_cliente = {col: globals()[col] for col in df_clientes.columns if col != 'id' and col != 'usuario'}
            new_cliente['usuario'] = username  # Adiciona o usuário atual como o inseridor
            supabase.table('clientes').insert(new_cliente).execute()
   
elif authentication_status == False:
    st.error('Nome de usuário/senha incorreto')
elif authentication_status == None:
    st.warning('Por favor, insira seu nome de usuário e senha')

