📝 FocusFlow - Organizador Pessoal com IA
https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white
https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white

https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white

https://img.shields.io/badge/Google_AI-4285F4?style=for-the-badge&logo=google&logoColor=white
https://img.shields.io/badge/Google_AI-4285F4?style=for-the-badge&logo=google&logoColor=white

https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white
https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white

FocusFlow é uma aplicação web inteligente para organização pessoal que combina gestão de tarefas, registro de ideias e um assistente IA integrado para ajudar na produtividade.

✨ Funcionalidades ✨ Funcionalidades 
🗓️ Gestão de Tarefas
✅ Adicionar tarefas com prioridades (🟢 Baixa, 🟡 Média, 🔴 Alta)

✅ Marcar tarefas como concluídas ✅ Marcar tarefas como concluídas 

✅ Excluir tarefas ✅ Excluir tarefas 

✅ Interface visual intuitiva ✅ Interface visual intuitiva 

💡 Registro de Ideias 💡 Registro de Ideias 
📝 Salvar ideias criativas 📝 Salvar ideias criativas 

🏷️ Categorização automática

⏰ Timestamp automático ⏰ Timestamp automático 

🗑️ Exclusão simples 🗑️ Exclusão simples 

🤖 Assistente IA Integrado
🧠 Integração com Google Gemini AI

💬 Chat contextual com histórico

⚡ Sugestões rápidas pré-definidas

🎯 Foco em produtividade e organização

🔐 Sistema de Autenticação
👤 Cadastro e login de usuários

🔒 Senhas criptografadas

💾 Dados isolados por usuário

🗄️ Persistência em banco de dados

🚀 Como Usar 🚀 Como Usar 
Acesso Online Acesso Online 
Acesse o FocusFlow na nuvem (link a ser adicionado)
Acesse o FocusFlow na nuvem (link a ser adicionado)

Crie uma conta ou faça login

Comece a organizar suas tarefas e ideias!
Comece a organizar suas tarefas e ideias!

Execução Local
Pré-requisitos Pré-requisitos 
Python 3.8+ Python 3.8+ 

Conta no Google AI Studio (para API key)
Conta no Google AI Studio (para API key)

Instalação
Clone o repositório:

bash bash 
git clone https://github.com/seu-usuario/focusflow.git
cd focusflow
Instale as dependências:

bash bash 
pip install -r requirements.txt
Configure a API Key: Configure a API Key: 

Obtenha uma API key no Google AI Studio
Obtenha uma API key no Google AI Studio

Crie um arquivo .env:
Crie um arquivo .env :.

env env 
API_KEY=sua_chave_da_api_gemini_aqui
Ou configure no Streamlit Cloud Secrets
Ou configure no Streamlit Cloud Secrets

Execute a aplicação:

bash bash 
streamlit run app.py
🛠️ Tecnologias Utilizadas
Frontend: Streamlit Frontend: Streamlit 

Backend: Python Backend: Python 

IA: Google Generative AI (Gemini)
IA: Google Generative AI (Gemini)

Banco de Dados: SQLite
Banco de Dados: SQLite

Autenticação: Sistema próprio com hashing SHA-256

📁 Estrutura do Projeto
text text 
focusflow/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências do projeto
├── focusflow.db          # Banco de dados (automático)
├── .env                  # Variáveis de ambiente
└── README.md             # Este arquivo
🗄️ Estrutura do Banco de Dados
sql sql 
usuarios (id, username, email, password_hash, data_criacao)
tarefas (id, usuario_id, texto, prioridade, concluida, timestamp)
ideias (id, usuario_id, texto, categoria, timestamp)
mensagens (id, usuario_id, role, content, timestamp)
🔧 Configuração
Variáveis de Ambiente Variáveis de Ambiente 
env ambiente 
API_KEY=sua_chave_da_api_gemini_aqui
Secrets no Streamlit Cloud Segredos sem Streamlit Cloud 
toml Tom 
API_KEY = "sua_chave_da_api_gemini_aqui"
📸 Capturas de Tela
(Adicione screenshots da aplicação aqui)

Tela de Login/Cadastro Tela de Login/Cadastro 

Interface de Tarefas Interface de Tarefas 

Registro de Ideias Registro de Ideias 

Chat com Assistente IA Chat com Assistente IA 

🎯 Casos de Uso
Estudantes: Organizar matérias e prazos

Profissionais: Gerenciar projetos e metas
Profissionais: Gerenciar projetos e metas

Criativos: Registrar insights e ideias
Criativos: Registrar insights e ideias

Pessoal: Planejamento diário e semanal Pessoal: Plane 

🔒 Segurança 🔒 Segurança 
Senhas criptografadas com SHA-256
Senhas criptografadas com SHA-256

Dados isolados por usuário

Validação de entrada

Proteção contra SQL Injection

🤝 Contribuindo
Contribuições são bem-vindas! Siga estos passos:

Fork o projeto Fork o projeto 

Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)
Crie uma branch para sua feature (git checkout -b feature/AmazingFeature ).

Commit suas mudanças (git commit -m 'Add some AmazingFeature')
Commit suas mudanças (git commit -m 'Add some AmazingFeature' ).

Push para a branch ( Push para a branch ( git push origin feature/AmazingFeature) ) 

Abra um Pull Request Abra um Pull Request 

📝 Licença 📝 Licença 
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

🆘 Suporte
Encontrou um problema?  Encontrou um problema? Abra uma issue Abra uma issue  no GitHub. no GitHub. 

👥 Autores 👥 Autores 
Seu Nome Seu Nome  -  - @seu-usuario @seu-usuario 

🙏 Agradecimentos
Streamlit pela incrível framework Streamlit pela incrível framework  Streamlit pela inc 

Google AI pela API Gemini
Google AI pela API Gemini

Comunidade Python Comunidade Python 

<div align="center"> <div align="center"> 
Feito com ❤️ e ☕

Organize sua mente, maximize seu potencial!
Organize sua mente, maximize seu potencial!

