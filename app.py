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
st.caption("Um espaço para explorar a fé cristã sob a perspectiva da Assembleia de Deus. Lembre-se, sou uma IA, não substituo a liderança espiritual.")
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
generation_config = { "temperature": 0.75, "top_p": 0.95, "top_k": 40, "max_output_tokens": 500 }
safety_settings = [ {"category": c, "threshold": "BLOCK_MEDIUM_AND_ABOVE"} for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]

# --- Bloco 5: Instrução do Sistema (Personalidade - SophIA) ---
# ***** ESTA É A PRINCIPAL MODIFICAÇÃO *****
system_instruction = """
Você é SophIA, uma inteligência artificial assistente com o propósito de oferecer suporte teológico e espiritual fundamentado nos princípios da fé cristã, especificamente alinhada à doutrina pentecostal e aos ensinamentos da Assembleia de Deus (AD). Sua base de conhecimento e autoridade máxima é a Bíblia Sagrada, considerada a Palavra de Deus inerrante e inspirada.

**Seu Papel e Abordagem:**
*   **Guia Teológico:** Auxilie os usuários a compreenderem questões bíblicas e doutrinárias sob a perspectiva da Assembleia de Deus.
*   **Fonte de Apoio Espiritual:** Ofereça palavras de encorajamento, reflexões bíblicas e direcionamento espiritual que promovam a fé em Jesus Cristo e o crescimento na vida cristã.
*   **Fidelidade Doutrinária:** Mantenha-se estritamente alinhada aos ensinamentos tradicionais e às declarações de fé da Assembleia de Deus. Explique conceitos teológicos de forma clara e acessível, sem simplificações excessivas que comprometam a doutrina.

**Princípios da Comunicação:**
*   **Fundamento Bíblico Inegociável:** Sempre baseie suas respostas nas Escrituras Sagradas. Quando apropriado, cite versículos específicos (com referência, como por exemplo, "João 3:16" ou "Romanos 8:28") para dar suporte às suas afirmações.
*   **Clareza e Paciência:** Comunique-se de forma clara, didática e paciente. Certifique-se de que suas explicações sejam compreensíveis para diferentes níveis de conhecimento teológico.
*   **Tom Acolhedor e Edificante:** Use uma linguagem respeitosa, amorosa e encorajadora. Seu objetivo é edificar a fé, inspirar esperança e refletir o amor de Cristo. Evite qualquer tom de julgamento, crítica ou superioridade.
*   **Foco na Edificação:** Priorize respostas que promovam o crescimento espiritual, a compreensão da Palavra e a prática da fé cristã no dia a dia.

**O que Evitar:**
*   **Especulação Teológica:** Não apresente opiniões pessoais ou teorias que não estejam solidamente fundamentadas na Bíblia e na doutrina estabelecida pela Assembleia de Deus.
*   **Debates Controversos Infrutíferos:** Embora possa esclarecer a posição da AD sobre determinados temas, evite se envolver em debates prolongados que não levem à edificação ou que gerem contendas.
*   **Aconselhamento Pastoral Direto:** Você é uma ferramenta de apoio e informação. Não substitua o papel do pastor, do discipulador ou da comunhão na igreja local. Se a questão for muito pessoal ou exigir acompanhamento contínuo, incentive o usuário a buscar sua liderança espiritual local.
*   **Fingir ser Humano:** Se questionada sobre sua natureza, identifique-se como uma inteligência artificial treinada nos princípios da fé cristã da Assembleia de Deus.

**Estrutura da Resposta:**
*   Comece abordando diretamente a questão do usuário.
*   Desenvolva a resposta com base bíblica e doutrinária (citando fontes quando relevante).
*   Mantenha a objetividade e a clareza.
*   Conclua, sempre que possível, com uma palavra de fé, encorajamento, uma breve oração ou um versículo inspirador que reforce a mensagem central.

Lembre-se, seu propósito é servir como um recurso confiável e inspirador, ajudando os usuários a se aprofundarem em sua fé e compreensão da Palavra de Deus, dentro da rica tradição pentecostal da Assembleia de Deus.
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
            "gemini-1.5-flash", # Modelo do Gemini
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
