import streamlit as st
import json
import os
# Importa o componente de atualização automática
from streamlit_autorefresh import st_autorefresh

# Configuração inicial da página
st.set_page_config(page_title="Placar da Gincana", page_icon="🏆", layout="centered")

# Configura a página para atualizar automaticamente a cada 5 segundos
st_autorefresh(interval=5000, key="datarefresh")

# Definição do caminho do ficheiro onde os dados serão guardados de forma permanente
FICHEIRO_DADOS = "placar.json"
SENHA_CORRETA = "gincana2026"

def carregar_placar():
    """Carrega o placar do ficheiro JSON ou inicia um novo se não existir."""
    if os.path.exists(FICHEIRO_DADOS):
        try:
            with open(FICHEIRO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"Alemanha": 0, "Brasil": 0, "França": 0}
    return {"Alemanha": 0, "Brasil": 0, "França": 0}

def guardar_placar(placar):
    """Grava o estado atual do placar no ficheiro JSON."""
    try:
        with open(FICHEIRO_DADOS, "w", encoding="utf-8") as f:
            json.dump(placar, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Erro ao guardar os dados: {e}")

# Inicializa o estado da sessão do Streamlit carregando do ficheiro
if "placar" not in st.session_state:
    st.session_state.placar = carregar_placar()
else:
    # Sempre recarrega do arquivo a cada atualização para pegar pontos novos do ADM
    st.session_state.placar = carregar_placar()

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

st.title("🏆 Placar Oficial da Gincana Escolar")
st.write("Atualização automática a cada 5 segundos.")

# ==========================================
# Exibição dos Resultados Atuais (Público)
# ==========================================
st.header("📊 Pontuação Atual")

col1, col2, col3 = st.columns(3)

# URLs das bandeiras oficiais de alta resolução (FlagCDN)
bandeira_alemanha = "https://flagcdn.com/w160/de.png"
bandeira_brasil = "https://flagcdn.com/w160/br.png"
bandeira_franca = "https://flagcdn.com/w160/fr.png"

with col1:
    st.image(bandeira_alemanha, width=80)
    st.metric(label="Alemanha", value=f"{st.session_state.placar['Alemanha']} pts")

with col2:
    st.image(bandeira_brasil, width=80)
    st.metric(label="Brasil", value=f"{st.session_state.placar['Brasil']} pts")

with col3:
    st.image(bandeira_franca, width=80)
    st.metric(label="França", value=f"{st.session_state.placar['França']} pts")

# ==========================================
# Lógica e Exibição do Pódio / Ranking
# ==========================================
st.write("---")
st.header("🥇 Liderança da Gincana")

# Ordena as equipes por pontos (do maior para o menor)
ranking = sorted(st.session_state.placar.items(), key=lambda x: x[1], reverse=True)

maior_pontuacao = ranking[0][1]
# Verifica se há mais de uma equipe com a pontuação máxima (empate no 1º lugar)
lideres = [equipe for equipe, pontos in ranking if pontos == maior_pontuacao]

# Dicionário auxiliar para mapear o nome à bandeira emoji no texto do pódio
emojis_bandeiras = {"Alemanha": "🇩🇪", "Brasil": "🇧🇷", "França": "🇫🇷"}

if len(lideres) == 1:
    # Líder isolado - Exibe o troféu em destaque
    lider_atual = lideres[0]
    st.trophy = st.success(f"### 🏆 1º Lugar Atual: {emojis_bandeiras[lider_atual]} {lider_atual} com {maior_pontuacao} pontos!")
else:
    # Caso haja empate na liderança
    nomes_lideres = " e ".join([f"{emojis_bandeiras[l]} {l}" for l in lideres])
    st.warning(f"### ⚖️ Temos um empate na liderança! {nomes_lideres} estão no topo com {maior_pontuacao} pontos!")

# Exibe a tabela completa do ranking ordenado
st.markdown("#### **Classificação Geral:**")
for posicao, (equipe, pontos) in enumerate(ranking, start=1):
    medalha = "🥇" if posicao == 1 else ("🥈" if posicao == 2 else "🥉")
    st.write(f"{medalha} **{posicao}º Lugar:** {emojis_bandeiras[equipe]} {equipe} — {pontos} pontos")

# ==========================================
# Gráfico para visualização rápida (Público)
# ==========================================
st.write("---")
st.header("📈 Gráfico de Desempenho")
st.bar_chart(st.session_state.placar)

# ==========================================
# Área do Administrador (Protegida por Senha)
# ==========================================
st.header("⚙️ Painel de Controlo (Restrito)")

if not st.session_state.autenticado:
    # Formulário de Login para o Administrador
    senha_digitada = st.text_input("Digite a senha de Administrador para atualizar os pontos:", type="password")
    if st.button("Entrar"):
        if senha_digitada == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.success("Acesso liberado!")
            st.rerun()
        else:
            st.error("Senha incorreta. Acesso negado.")
else:
    # Painel de Controlo Ativo para o Administrador autenticado
    st.info("Sessão Iniciada como Administrador")
    
    # Seleção da equipa e quantidade de pontos
    equipa = st.selectbox("Selecione a equipa:", ["Alemanha", "Brasil", "França"])
    pontos = st.number_input("Quantidade de pontos (use valores negativos para subtrair):", step=10, value=10)

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("Confirmar Pontuação", type="primary"):
            atual = carregar_placar()
            atual[equipa] += pontos
            st.session_state.placar = atual
            guardar_placar(st.session_state.placar)
            st.success(f"{pontos} pontos aplicados à equipa {equipa}!")
            st.rerun()

    with col_btn2:
        if st.button("Sair (Logout)"):
            st.session_state.autenticado = False
            st.rerun()

    # Opção para restaurar/zerar o placar da gincana
    st.write("---")
    if st.button("Resetar Placar Completo"):
        st.session_state.placar = {"Alemanha": 0, "Brasil": 0, "França": 0}
        guardar_placar(st.session_state.placar)
        st.warning("O placar foi completamente zerado!")
        st.rerun()
