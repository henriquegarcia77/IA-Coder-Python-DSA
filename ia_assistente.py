#Importando bibliotecas
import os
import streamlit as st

from groq import Groq

#Configurando página do Streamlit 
st.set_page_config(
    page_title = "IA CODER",
    page_icon = "📖",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

CUSTOM_PROMPT ="""""
1. **Foco em Programação**
   - Responda **exclusivamente** a perguntas relacionadas a:
     - Programação
     - Algoritmos
     - Estruturas de dados
     - Lógica computacional
     - Ciência de dados
     - Automação
     - Boas práticas de desenvolvimento
   - Caso a pergunta não esteja relacionada a esses temas, informe educadamente que está fora do escopo.

2. **Estrutura da Resposta**
   Sempre organize suas respostas seguindo obrigatoriamente o formato abaixo:

   **1️⃣ Explicação Clara**
   - Inicie com uma explicação conceitual do tema solicitado.
   - Seja direto, objetivo e didático.
   - Utilize exemplos simples quando necessário.

   **2️⃣ Exemplo de Código**
   - Forneça um ou mais blocos de código **em Python**, utilizando sintaxe correta.
   - O código deve ser funcional, legível e bem estruturado.
   - Utilize boas práticas, como nomes de variáveis claros e indentação adequada.

   **3️⃣ Detalhes do Código**
   - Explique detalhadamente o que cada parte do código faz.
   - Descreva o fluxo lógico, funções, estruturas de controle e possíveis variações.
   - Caso existam alternativas ou otimizações, mencione.

   **4️⃣ Documentação de Referência**
   - Ao final, inclua uma seção chamada **"📚 Documentação de Referência"**
   - Cite documentações oficiais, bibliotecas ou conceitos relevantes (ex: Python Docs, Pandas, NumPy, etc.).

3. **Clareza e Precisão**
   - Utilize linguagem clara e acessível.
   - Evite jargões desnecessários.
   - Seja técnico apenas quando necessário.
   - Priorize precisão, legibilidade e organização.

4. **Boas Práticas**
   - Sempre que possível, destaque boas práticas de programação.
   - Alerte sobre erros comuns.
   - Sugira melhorias ou extensões do código apresentado.

5. **Idioma**
   - Responda sempre em **português (Brasil)**, salvo se o usuário solicitar outro idioma.
"""""

#Criar interface
with st.sidebar: #Criando a barrra lateral e os componentes
    st.title("IA Coder") #Titulo da barra lateral

    st.markdown("Assistente de IA") #Texto explicativo

    groq_api_key = st.text_input(   #Campo para digitar chave API
        "Insira sua Key",
        type = "password",
        help = " Obtenha sua chave:https://console.groq.com/keys"   #Botão de ajuda
    )

    st.markdown("---") #Estilização da interface
    st.markdown("Desenvolvido para ajudar em dúvidas de Python")

    st.markdown("---")
    st.markdown("Meu perfil no linkedin")
    st.markdown("https://www.linkedin.com/in/rikegb/")

    #Cada st.markdow seria como um parágrafo

#Estilizando o centro da interface com título, subtítulo e texto de apoio
st.title("AI Coder")
st.title("Assistente pessoal")
st.caption("Faça uma pergunta sobre a Linguagem Python")

#Configurar o histórico das mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message["content"])


#Configurar comunicação do input para o groq
client = None

if groq_api_key:    #Verificar se digitou key

    try:
        client = Groq(api_key = groq_api_key)

    except Exception as e: #Exibir erro caso tenha
        st.sidebar.error(f"Erro ao inicializar: {e}")
        st.stop()
elif st.session_state.messages:
    st.warning("Insira uma key")

elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada do usuário no chat
if prompt := st.chat_input("Qual sua dúvida sobre Python?"):
    
    # Se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara mensagens para enviar à API, incluindo prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):
            
            try:
                
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extrai a resposta gerada pela API
                dsa_ai_resposta = chat_completion.choices[0].message.content
                
                # Exibe a resposta no Streamlit
                st.markdown(dsa_ai_resposta)
                
                # Armazena resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            # Caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p> AI Coder - Parte Integrante do Curso Gratuito Fundamentos de Linguagem Python da Data Science Academy</p>
    </div>
    """,
    unsafe_allow_html=True
)

