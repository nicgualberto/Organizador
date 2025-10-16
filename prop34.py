import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime, date

# Configuração da página
st.set_page_config(
    page_title="Organizador Diário IA",
    page_icon="📝",
    layout="centered"
)

# Configuração do tema azul
st.markdown("""
    <style>
    .main {
        background-color: #1e3a8a;
    }
    .stApp {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
    }
    .header {
        color: white;
        text-align: center;
        padding: 1rem;
    }
    .task-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        backdrop-filter: blur(10px);
    }
    .idea-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #60a5fa;
        backdrop-filter: blur(10px);
    }
    .assistant-message {
        background-color: rgba(255, 255, 255, 0.15);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px 8px 0px 0px;
        gap: 8px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Configuração da API
try:
    key = os.getenv("API_KEY")
    genai.configure(api_key=st.secrets["API_KEY"])
except:
    st.error("⚠️ API KEY não configurada. Configure suas credenciais.")
    st.stop()

# Inicialização do estado da sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "tarefas" not in st.session_state:
    st.session_state.tarefas = []
if "ideias" not in st.session_state:
    st.session_state.ideias = []

# Header
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("📝 Organizador Diário IA")
st.markdown(f"### {date.today().strftime('%d/%m/%Y')}")
st.markdown("</div>", unsafe_allow_html=True)

# Layout com abas
tab1, tab2, tab3 = st.tabs(["🗓️ Tarefas", "💡 Ideias", "🤖 Assistente IA"])

with tab1:
    st.subheader("📋 Minhas Tarefas")
    
    # Formulário para adicionar tarefa
    with st.form("nova_tarefa", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            nova_tarefa = st.text_input("Nova tarefa:", placeholder="Ex: Reunião com equipe às 10h")
        with col2:
            prioridade = st.selectbox("Prioridade:", ["🟢 Baixa", "🟡 Média", "🔴 Alta"])
        
        submitted = st.form_submit_button("Adicionar Tarefa")
        
        if submitted and nova_tarefa:
            st.session_state.tarefas.append({
                "texto": nova_tarefa,
                "prioridade": prioridade,
                "concluida": False,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    # Lista de tarefas
    if st.session_state.tarefas:
        for i, tarefa in enumerate(st.session_state.tarefas):
            st.markdown(f'<div class="task-card">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([6, 2, 2])
            with col1:
                if tarefa["concluida"]:
                    st.markdown(f"~~{tarefa['texto']}~~")
                else:
                    st.write(f"{tarefa['texto']}")
            with col2:
                st.write(tarefa["prioridade"])
            with col3:
                if not tarefa["concluida"]:
                    if st.button("✅", key=f"concluir_{i}"):
                        st.session_state.tarefas[i]["concluida"] = True
                        st.rerun()
                if st.button("🗑️", key=f"excluir_{i}"):
                    st.session_state.tarefas.pop(i)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🎉 Nenhuma tarefa pendente! Adicione uma nova tarefa acima.")

with tab2:
    st.subheader("💭 Minhas Ideias")
    
    # Formulário para adicionar ideia
    with st.form("nova_ideia", clear_on_submit=True):
        nova_ideia = st.text_area("Nova ideia:", placeholder="Ex: Ideia para novo projeto...", height=100)
        submitted = st.form_submit_button("Salvar Ideia")
        
        if submitted and nova_ideia:
            st.session_state.ideias.append({
                "texto": nova_ideia,
                "timestamp": datetime.now().strftime("%H:%M"),
                "categoria": "Geral"
            })
            st.rerun()
    
    # Lista de ideias
    if st.session_state.ideias:
        for i, ideia in enumerate(st.session_state.ideias):
            st.markdown(f'<div class="idea-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([8, 2])
            with col1:
                st.write(ideia["texto"])
                st.caption(f"⏰ {ideia['timestamp']}")
            with col2:
                if st.button("🗑️", key=f"excluir_ideia_{i}"):
                    st.session_state.ideias.pop(i)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 Nenhuma ideia salva ainda. Registre suas ideias criativas!")

with tab3:
    st.subheader("🤖 Assistente de Organização IA")
    
    # Mostrar histórico do chat
    for msg in st.session_state.mensagens:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.markdown(f'<div class="assistant-message">', unsafe_allow_html=True)
            st.write(msg["content"])
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Sugestões rápidas
    st.markdown("**Sugestões rápidas:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Planejar dia"):
            st.session_state.mensagens.append({
                "role": "user", 
                "content": "Me ajude a planejar meu dia de forma produtiva"
            })
            st.rerun()
    
    with col2:
        if st.button("💡 Brainstorm"):
            st.session_state.mensagens.append({
                "role": "user", 
                "content": "Me ajude a fazer um brainstorm de ideias criativas"
            })
            st.rerun()
    
    with col3:
        if st.button("📊 Prioridades"):
            st.session_state.mensagens.append({
                "role": "user", 
                "content": "Me ajude a definir minhas prioridades"
            })
            st.rerun()
    
    # Input do usuário
    user_input = st.chat_input("Pergunte ao assistente sobre organização, produtividade...")
    
    if user_input:
        # Adicionar mensagem do usuário
        st.chat_message("user").write(user_input)
        st.session_state.mensagens.append({"role": "user", "content": user_input})
        
        # Criar contexto com informações das tarefas e ideias
        contexto = f"""
        Hoje é {date.today().strftime('%d/%m/%Y')}.
        
        Tarefas do usuário: {[t['texto'] for t in st.session_state.tarefas if not t['concluida']]}
        Ideias do usuário: {[i['texto'] for i in st.session_state.ideias]}
        
        Histórico da conversa: {st.session_state.mensagens[-5:]}
        
        Usuário pergunta: {user_input}
        
        Você é um assistente especializado em organização, produtividade e gestão de tarefas. 
        Responda de forma útil e motivacional, focando em ajudar com organização pessoal.
        """
        
        # Gerar resposta
        with st.spinner("🤔 Pensando na melhor forma de ajudar..."):
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                resposta = model.generate_content(contexto)
                resposta_ia = resposta.text
                
                # Adicionar resposta ao histórico
                st.markdown(f'<div class="assistant-message">', unsafe_allow_html=True)
                st.write(resposta_ia)
                st.markdown('</div>', unsafe_allow_html=True)
                st.session_state.mensagens.append({
                    "role": "assistant", 
                    "content": resposta_ia
                })
                
            except Exception as e:
                st.error(f"Erro ao conectar com a IA: {e}")

# Footer
st.markdown("---")
st.caption("✨ Organizador Diário IA - Mantenha suas ideias e tarefas organizadas")
