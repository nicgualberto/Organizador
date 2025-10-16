import streamlit as st
import google.generativeai as genai
import os
import sqlite3
import hashlib
from datetime import datetime, date

try:
    import google.generativeai as genai
except ImportError:
    st.error("""
    📦 Biblioteca necessária não encontrada!
    
    Para instalar, execute no terminal:
    ```bash
    pip install google-generativeai
    ```
    """)
    st.stop()

# Configuração da página
st.set_page_config(
    page_title="FocusFlow",
    page_icon="📝",
    layout="centered"
)

# CSS personalizado
st.markdown("""
    <style>
    .header {
        text-align: center;
        padding: 1rem;
    }
    .task-card {
        background-color: var(--background-color);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
    }
    .idea-card {
        background-color: var(--background-color);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #60a5fa;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
    }
    .assistant-message {
        background-color: var(--secondary-background-color);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid var(--border-color);
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Configuração da API
api_key = os.getenv("API_KEY")
genai.configure(api_key=st.secrets["API_KEY"])

# Sistema de Banco de Dados
class DatabaseManager:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        """Inicializa o banco de dados e cria tabelas se não existirem"""
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de tarefas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                texto TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                concluida BOOLEAN DEFAULT FALSE,
                timestamp TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Tabela de ideias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ideias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                texto TEXT NOT NULL,
                categoria TEXT DEFAULT 'Geral',
                timestamp TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Tabela de mensagens do chat
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Gera hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def criar_usuario(self, username, email, password):
        """Cria um novo usuário"""
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                'INSERT INTO usuarios (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def verificar_login(self, username, password):
        """Verifica credenciais de login"""
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            'SELECT id, username FROM usuarios WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario:
            return {'id': usuario[0], 'username': usuario[1]}
        return None
    
    # Operações para Tarefas
    def salvar_tarefa(self, usuario_id, tarefa):
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO tarefas (usuario_id, texto, prioridade, concluida, timestamp) VALUES (?, ?, ?, ?, ?)',
            (usuario_id, tarefa['texto'], tarefa['prioridade'], tarefa['concluida'], tarefa['timestamp'])
        )
        
        conn.commit()
        conn.close()
    
    def carregar_tarefas(self, usuario_id):
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT texto, prioridade, concluida, timestamp FROM tarefas WHERE usuario_id = ? ORDER BY data_criacao DESC',
            (usuario_id,)
        )
        
        tarefas = []
        for row in cursor.fetchall():
            tarefas.append({
                'texto': row[0],
                'prioridade': row[1],
                'concluida': bool(row[2]),
                'timestamp': row[3]
            })
        
        conn.close()
        return tarefas
    
    def atualizar_tarefa(self, usuario_id, index, campo, valor):
        tarefas = self.carregar_tarefas(usuario_id)
        if 0 <= index < len(tarefas):
            # Para simplificar, recriamos a lista
            self.limpar_tarefas(usuario_id)
            tarefas[index][campo] = valor
            for tarefa in tarefas:
                self.salvar_tarefa(usuario_id, tarefa)
    
    def excluir_tarefa(self, usuario_id, index):
        tarefas = self.carregar_tarefas(usuario_id)
        if 0 <= index < len(tarefas):
            self.limpar_tarefas(usuario_id)
            tarefas.pop(index)
            for tarefa in tarefas:
                self.salvar_tarefa(usuario_id, tarefa)
    
    def limpar_tarefas(self, usuario_id):
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tarefas WHERE usuario_id = ?', (usuario_id,))
        conn.commit()
        conn.close()
    
    # Operações para Ideias
    def salvar_ideia(self, usuario_id, ideia):
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO ideias (usuario_id, texto, categoria, timestamp) VALUES (?, ?, ?, ?)',
            (usuario_id, ideia['texto'], ideia['categoria'], ideia['timestamp'])
        )
        
        conn.commit()
        conn.close()
    
    def carregar_ideias(self, usuario_id):
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT texto, categoria, timestamp FROM ideias WHERE usuario_id = ? ORDER BY data_criacao DESC',
            (usuario_id,)
        )
        
        ideias = []
        for row in cursor.fetchall():
            ideias.append({
                'texto': row[0],
                'categoria': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return ideias
    
    def excluir_ideia(self, usuario_id, index):
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id FROM ideias WHERE usuario_id = ? ORDER BY data_criacao DESC LIMIT 1 OFFSET ?',
            (usuario_id, index)
        )
        
        resultado = cursor.fetchone()
        if resultado:
            cursor.execute('DELETE FROM ideias WHERE id = ?', (resultado[0],))
            conn.commit()
        
        conn.close()
    
    # Operações para Mensagens
    def salvar_mensagem(self, usuario_id, role, content):
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO mensagens (usuario_id, role, content) VALUES (?, ?, ?)',
            (usuario_id, role, content)
        )
        
        conn.commit()
        conn.close()
    
    def carregar_mensagens(self, usuario_id, limite=50):
        conn = sqlite3.connect('focusflow.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT role, content FROM mensagens WHERE usuario_id = ? ORDER BY timestamp DESC LIMIT ?',
            (usuario_id, limite)
        )
        
        mensagens = []
        for row in cursor.fetchall():
            mensagens.append({
                'role': row[0],
                'content': row[1]
            })
        
        conn.close()
        return mensagens[::-1]  # Reverter para ordem cronológica

# Inicializar banco de dados
db = DatabaseManager()

# Sistema de Autenticação
def mostrar_tela_login():
    """Mostra tela de login/cadastro"""
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.title("🔐 FocusFlow")
    
    tab_login, tab_cadastro = st.tabs(["🚪 Login", "📝 Cadastro"])
    
    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            login_submitted = st.form_submit_button("Entrar")
            
            if login_submitted:
                if username and password:
                    usuario = db.verificar_login(username, password)
                    if usuario:
                        st.session_state.usuario = usuario
                        st.session_state.logado = True
                        carregar_dados_usuario(usuario['id'])
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos!")
                else:
                    st.warning("Preencha todos os campos!")
    
    with tab_cadastro:
        with st.form("cadastro_form"):
            new_username = st.text_input("Novo usuário")
            new_email = st.text_input("Email")
            new_password = st.text_input("Nova senha", type="password")
            confirm_password = st.text_input("Confirmar senha", type="password")
            cadastro_submitted = st.form_submit_button("Criar conta")
            
            if cadastro_submitted:
                if new_username and new_email and new_password:
                    if new_password == confirm_password:
                        if db.criar_usuario(new_username, new_email, new_password):
                            st.success("Conta criada com sucesso! Faça login.")
                        else:
                            st.error("Usuário ou email já existem!")
                    else:
                        st.error("Senhas não coincidem!")
                else:
                    st.warning("Preencha todos os campos!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def carregar_dados_usuario(usuario_id):
    """Carrega todos os dados do usuário do banco de dados"""
    st.session_state.tarefas = db.carregar_tarefas(usuario_id)
    st.session_state.ideias = db.carregar_ideias(usuario_id)
    st.session_state.mensagens = db.carregar_mensagens(usuario_id)

def salvar_tarefa_usuario(tarefa):
    """Salva tarefa no banco de dados"""
    db.salvar_tarefa(st.session_state.usuario['id'], tarefa)

def salvar_ideia_usuario(ideia):
    """Salva ideia no banco de dados"""
    db.salvar_ideia(st.session_state.usuario['id'], ideia)

def salvar_mensagem_usuario(role, content):
    """Salva mensagem no banco de dados"""
    db.salvar_mensagem(st.session_state.usuario['id'], role, content)

# Inicialização do estado da sessão
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "tarefas" not in st.session_state:
    st.session_state.tarefas = []
if "ideias" not in st.session_state:
    st.session_state.ideias = []

# Verificar autenticação
if not st.session_state.logado:
    mostrar_tela_login()
    st.stop()

# APLICAÇÃO PRINCIPAL (após login)
# Header
st.markdown('<div class="header">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.title(f"📝 FocusFlow - {st.session_state.usuario['username']}")
with col2:
    st.markdown(f"### {date.today().strftime('%d/%m/%Y')}")
with col3:
    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.session_state.usuario = None
        st.rerun()
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
            tarefa_data = {
                "texto": nova_tarefa,
                "prioridade": prioridade,
                "concluida": False,
                "timestamp": datetime.now().strftime("%H:%M")
            }
            salvar_tarefa_usuario(tarefa_data)
            st.session_state.tarefas.append(tarefa_data)
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
                        db.atualizar_tarefa(st.session_state.usuario['id'], i, "concluida", True)
                        st.session_state.tarefas[i]["concluida"] = True
                        st.rerun()
                if st.button("🗑️", key=f"excluir_{i}"):
                    db.excluir_tarefa(st.session_state.usuario['id'], i)
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
            ideia_data = {
                "texto": nova_ideia,
                "timestamp": datetime.now().strftime("%H:%M"),
                "categoria": "Geral"
            }
            salvar_ideia_usuario(ideia_data)
            st.session_state.ideias.append(ideia_data)
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
                    db.excluir_ideia(st.session_state.usuario['id'], i)
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
            user_msg = "Me ajude a planejar meu dia de forma produtiva"
            st.session_state.mensagens.append({"role": "user", "content": user_msg})
            salvar_mensagem_usuario("user", user_msg)
            st.rerun()
    
    with col2:
        if st.button("💡 Brainstorm"):
            user_msg = "Me ajude a fazer um brainstorm de ideias criativas"
            st.session_state.mensagens.append({"role": "user", "content": user_msg})
            salvar_mensagem_usuario("user", user_msg)
            st.rerun()
    
    with col3:
        if st.button("📊 Prioridades"):
            user_msg = "Me ajude a definir minhas prioridades"
            st.session_state.mensagens.append({"role": "user", "content": user_msg})
            salvar_mensagem_usuario("user", user_msg)
            st.rerun()
    
    # Input do usuário
    user_input = st.chat_input("Pergunte ao assistente sobre organização, produtividade...")
    
    if user_input:
        # Adicionar mensagem do usuário
        st.chat_message("user").write(user_input)
        st.session_state.mensagens.append({"role": "user", "content": user_input})
        salvar_mensagem_usuario("user", user_input)
        
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
                salvar_mensagem_usuario("assistant", resposta_ia)
                
            except Exception as e:
                st.error(f"Erro ao conectar com a IA: {e}")

# Footer
st.markdown("---")
st.caption(f"✨ FocusFlow - Organizador pessoal de {st.session_state.usuario['username']}")
