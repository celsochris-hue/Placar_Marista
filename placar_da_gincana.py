import streamlit as st

# Configuração inicial da página com layout otimizado
st.set_page_config(
    page_title="Placar da Gincana Escolar", 
    page_icon="🏆", 
    layout="centered"
)

# Defina a senha do administrador aqui
SENHA_CORRETA = "gincana2026"

# Inicialização de variáveis globais de estado
if "placar" not in st.session_state:
    st.session_state.placar = {"Alemanha": 0, "Brasil": 0, "França": 0}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Estilo CSS personalizado para alinhar as bandeiras e métricas de forma harmônica
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: -10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 Placar Oficial da Gincana")
st.write("Acompanhe o desempenho das equipes em tempo real!")

st.write("---")

# ==========================================
# Exibição dos Resultados Atuais (Público)
# ==========================================
st.header("📊 Pontuação Atual")

col1, col2, col3 = st.columns(3)

# Links oficiais das bandeiras (SVG/PNG via FlagCDN)
flag_urls = {
    "Alemanha": "https://flagcdn.com/w160/de.png",
    "Brasil": "https://flagcdn.com/w160/br.png",
    "França": "https://flagcdn.com/w160/fr.png"
}

with col1:
    st.image(flag_urls["Alemanha"], width=100)
    st.metric(label="Alemanha", value=f"{st.session_state.placar['Alemanha']} pts")

with col2:
    st.image(flag_urls["Brasil"], width=100)
    st.metric(label="Brasil", value=f"{st.session_state.placar['Brasil']} pts")

with col3:
    st.image(flag_urls["França"], width=100)
    st.metric(label="França", value=f"{st.session_state.placar['França']} pts")

st.write("---")

# ==========================================
# Gráfico para visualização rápida (Público)
# ==========================================
st.header("📈 Gráfico de Desempenho")
st.bar_chart(st.session_state.placar)

st.write("---")

# ==========================================
# Área do Administrador (Com Login e Logout)
# ==========================================
st.header("🔐 Área do Administrador")

# Caso o administrador NÃO esteja logado, exibe os campos de Login
if not st.session_state.logged_in:
    senha_digitada = st.text_input("Senha de acesso:", type="password", placeholder="Digite a senha do painel")
    
    if st.button("Entrar"):
        if senha_digitada == SENHA_CORRETA:
            st.session_state.logged_in = True
            st.success("Login efetuado com sucesso!")
            st.rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")

# Caso o administrador ESTEJA logado, libera o painel de edição
else:
    st.info("🔓 Você está logado no modo de edição.")
    
    # Seleção da equipe e quantidade de pontos
    equipe = st.selectbox("Selecione a equipe para pontuar:", ["Alemanha", "Brasil", "França"])
    pontos = st.number_input("Pontos (use números negativos para retirar):", step=10, value=10)

    # Botões de ação em colunas para uma interface mais compacta
    b_col1, b_col2 = st.columns(2)
    
    with b_col1:
        if st.button("Confirmar Pontuação", type="primary"):
            st.session_state.placar[equipe] += pontos
            st.success(f"Adicionado {pontos} pts para {equipe}!")
            st.rerun()
            
    with b_col2:
        if st.button("Zerar Placar (Reset)", help="Zera toda a pontuação do zero"):
            st.session_state.placar = {"Alemanha": 0, "Brasil": 0, "França": 0}
            st.warning("O placar foi zerado!")
            st.rerun()

    st.write("---")
    
    # Botão de Logout para fechar a sessão de administração com segurança
    if st.button("Sair (Logout)", type="secondary"):
        st.session_state.logged_in = False
        st.success("Sessão finalizada.")
        st.rerun()