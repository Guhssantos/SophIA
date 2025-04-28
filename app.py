# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import time

# --- Bloco 1: Configuração da Página ---
# Atualizado para SophIA
st.set_page_config(
    page_title="SophIA - Assistente Teológica", page_icon="📖", layout="centered", initial_sidebar_state="collapsed"
)

# --- Bloco 2: Título e Descrição ---
# Atualizado para SophIA
st.title("📖 SophIA: Sua Assistente Teológica")
st.caption("Um espaço para explorar a fé cristã sob a perspectiva da Assembleia de Deus.")
st.divider()

# --- Bloco 3: Configuração da API Key (MODIFICADO para Streamlit Cloud) ---
# (Sem alterações - estrutura reutilizada)
try:
    # O nome 'GOOGLE_API_KEY' aqui deve ser EXATAMENTE o mesmo
    # que você usará nos segredos do Streamlit Cloud.
    GOOGLE_API_KEY_APP = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY_APP)
    api_key_configured_app = True
except KeyError:
    st.error("Ops! Parece que a Chave API do Google não foi configurada nos 'Secrets' do Streamlit. Peça ajuda para configurá-la nas definições do app.")
    st.stop()
except Exception as e:
    st.error(f"Erro inesperado ao configurar a API Key: {e}")
    st.stop()

# --- Bloco 4: Configuração do Modelo Gemini ---
# (Sem alterações - estrutura reutilizada)
generation_config = {
    "temperature": 0.7, # Ajuste para mais criatividade vs. mais factualidade
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048, # Ajuste conforme necessário
}

safety_settings = [ # Ajuste os níveis de segurança conforme o caso de uso
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
# --- Bloco 5: Instrução do Sistema (Personalidade - SophIA) ---
# ***** ESTA É A PRINCIPAL MODIFICAÇÃO *****
system_instruction = """
Você é SophIA, uma assistente virtual cristã projetada para oferecer suporte teológico e espiritual, guiada pelos princípios da Assembleia de Deus no Brasil. Sua função é atuar como uma guia confiável e informada, refletindo a sabedoria encontrada na Bíblia Sagrada e alinhando-se à doutrina pentecostal. Sua comunicação deve ser: Clara e paciente, garantindo que todos compreendam a mensagem. Baseada firmemente na Palavra de Deus (priorizando a versão Almeida Revista e Corrigida - ARC), com citações bíblicas relevantes. Edificadora e inspiradora, enfatizando fé, amor e a mensagem de Jesus Cristo. Evite especulações teológicas que não estejam claramente fundamentadas nas Escrituras e mantenha suas respostas estritamente dentro do ensino tradicional da Assembleia de Deus, promovendo sempre a edificação espiritual dos usuários.

Instruções:
1.  **Fundamento Bíblico:** Sempre baseie as respostas na Bíblia Sagrada (priorizando a ARC), citando versículos pertinentes e seguindo fielmente a doutrina pentecostal da Assembleia de Deus.
2.  **Comunicação Clara e Acolhedora:** Use um tom respeitoso, paciente, empático e edificante. Jamais critique, julgue ou menospreze o usuário ou outras crenças.
3.  **Fidelidade Doutrinária:** Explique os princípios e doutrinas da Assembleia de Deus de forma clara e acessível, simplificando conceitos teológicos complexos sem distorcer seu significado original.
4.  **Resolução de Dúvidas:** Ao responder dúvidas, apresente a posição doutrinária estabelecida pela Assembleia de Deus. Evite entrar em debates teológicos prolongados ou controversos que não sejam produtivos para o crescimento espiritual.
5.  **Estilo de Resposta:** Seja objetiva e bem estruturada em suas respostas. Conclua com uma mensagem apropriada de fé, esperança ou encorajamento baseado nos princípios bíblicos.
6.  **Não Aconselhamento Pessoal:** Não forneça aconselhamento direto para problemas pessoais (financeiros, relacionais, saúde mental, etc.). Em vez disso, ofereça princípios bíblicos relevantes e incentive a busca por orientação pastoral ou profissional quando apropriado.
7.  **Reconhecimento de Limites:** Se uma pergunta for excessivamente complexa, fora do escopo teológico definido, ou se a resposta não for claramente estabelecida, admita a limitação com humildade e evite especulações. Sugira gentilmente que o usuário consulte um pastor ou líder espiritual.
"""

# --- Bloco 6: Definições de Segurança (CVV) ---
# (Sem alterações - ESSENCIAL manter esta segurança)
keywords_risco = [ "me matar", "me mate", "suicidio", "suicídio", "não aguento mais viver", "quero morrer", "queria morrer", "quero sumir", "desistir de tudo", "acabar com tudo", "fazer mal a mim", "me cortar", "me machucar", "automutilação" ]
resposta_risco_padrao = ( "Sinto muito que você esteja passando por um momento tão difícil e pensando nisso. É muito importante buscar ajuda profissional agora. Por favor, entre em contato com o CVV (Centro de Valorização da Vida) ligando para o número 188. A ligação é gratuita e eles estão disponíveis 24 horas por dia para conversar com você de forma sigilosa. Você não está sozinho(a) e há pessoas prontas para te ouvir." )

# --- Bloco 7: Função para Inicializar o Modelo ---
# (Sem alterações - estrutura reutilizada)
@st.cache_resource # Guarda o modelo na memória para não recarregar toda hora
def init_model():
    try:
        model = genai.GenerativeModel(
            "gemini-1.5-pro-latest", # Modelo do Gemini
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=system_instruction # Passa a personalidade da SophIA aqui
        )
        return model
    except Exception as e:
        st.error(f"Erro grave ao carregar o modelo de IA: {e}")
        st.stop()
model = init_model()

# --- Bloco 8: Gerenciamento do Histórico da Conversa ---
# (Estrutura reutilizada, mensagem inicial atualizada)
if "messages" not in st.session_state:
    # Mensagem inicial da SophIA
    st.session_state.messages = [{"role": "assistant", "content": "Olá! Sou SophIA. Em que posso ajudá-lo hoje com base na Palavra de Deus e nos ensinamentos da Assembleia de Deus?"}]
# Inicia a sessão de chat com o Gemini se não existir
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[]) # Histórico inicial vazio, pois a personalidade já está no modelo

# --- Bloco 9: Exibição do Histórico ---
# (Sem alterações - estrutura reutilizada)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Bloco 10: Input e Lógica Principal ---
# (Estrutura reutilizada, texto do spinner atualizado)
if prompt := st.chat_input("Digite sua dúvida ou reflexão..."):
    # Adiciona a mensagem do usuário ao histórico e mostra na tela
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Verifica se a mensagem contém palavras de risco (ESSENCIAL manter)
    prompt_lower = prompt.lower() # Converte para minúsculas para facilitar a busca
    contem_risco = any(keyword in prompt_lower for keyword in keywords_risco)

    if contem_risco:
        # Se contém risco, mostra a mensagem do CVV e NÃO envia para a IA
        with st.chat_message("assistant"):
            st.warning("Importante: Se você está passando por pensamentos difíceis ou de risco, por favor, busque ajuda profissional imediatamente.")
            st.markdown(resposta_risco_padrao)
        # Adiciona a resposta de risco ao histórico
        st.session_state.messages.append({"role": "assistant", "content": resposta_risco_padrao})
    else:
        # Se NÃO contém risco, envia para a IA processar
        try:
            # Texto do spinner atualizado para SophIA
            with st.spinner("SophIA está processando... 📖"):
                response = st.session_state.chat_session.send_message(prompt)
            bot_response = response.text
            # Adiciona a resposta da IA ao histórico e mostra na tela
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                # Efeito de digitação para a resposta da IA
                message_placeholder = st.empty()
                full_response = ""
                for chunk in bot_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05) # Pequena pausa para simular digitação
                    message_placeholder.markdown(full_response + "▌") # Mostra o cursor piscando
                message_placeholder.markdown(full_response) # Mostra a resposta completa

        except Exception as e:
            # Se der erro ao falar com a IA
            error_msg_user = f"Desculpe, ocorreu um problema técnico ao processar sua mensagem. Tente novamente mais tarde."
            st.error(error_msg_user)
            # Adiciona uma mensagem de erro genérica ao histórico
            error_response = "Sinto muito, tive um problema técnico interno. Por favor, tente novamente. 😔"
            st.session_state.messages.append({"role": "assistant", "content": error_response})
            print(f"ERRO DEBUG App: Falha Gemini - {e}") # Log técnico (não visível ao usuário)

# --- Bloco 11: Rodapé ---
# Atualizado para SophIA
st.divider()
st.caption("SophIA é uma ferramenta de IA para apoio teológico e espiritual.")

# --- Fim do app.py ---
