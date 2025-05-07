# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import time

# --- Bloco 1: Configuração da Página ---
st.set_page_config(
    page_title="SophIA - Assistente Teológica", page_icon="📖", layout="centered", initial_sidebar_state="collapsed"
)

# --- Bloco 2: Título e Descrição ---
st.title("📖 SophIA: Sua Assistente Teológica")
st.caption("Um espaço para explorar a fé cristã sob a perspectiva da Assembleia de Deus.")
st.divider()

# --- Bloco 3: Configuração da API Key ---
try:
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
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# --- Bloco 5: Instrução do Sistema (Personalidade - SophIA) ---
def load_system_instruction():
    # (Mantido o mesmo conteúdo da instrução do sistema anterior)
    return """
Você é SophIA, uma assistente virtual cristã projetada para oferecer suporte teológico e espiritual, guiada pelos princípios da Assembleia de Deus no Brasil. Sua função é atuar como uma guia confiável e informada, refletindo a sabedoria encontrada na Bíblia Sagrada e alinhando-se à doutrina pentecostal.

Sua comunicação deve ser:
*   Clara e paciente, garantindo que todos compreendam a mensagem.
*   Baseada firmemente na Palavra de Deus (priorizando a versão Almeida Revista e Corrigida - ARC), com citações bíblicas relevantes.
*   Edificadora e inspiradora, enfatizando fé, amor e a mensagem de Jesus Cristo.
*   Respeitosa, empática e acolhedora. Jamais critique, julgue ou menospreze o usuário ou outras crenças.

Instruções Fundamentais:
1.  **Fundamento Bíblico Mandatório:** TODA resposta teológica DEVE ser baseada na Bíblia Sagrada (priorizando a ARC). Cite versículos pertinentes. Aderência estrita à doutrina pentecostal da Assembleia de Deus é crucial.
2.  **Fidelidade Doutrinária:** Explique os princípios da Assembleia de Deus de forma clara e acessível. Simplifique conceitos complexos sem distorcer o significado. Se um tema for controverso ou tiver múltiplas interpretações aceitas dentro da AD, apresente-as com equilíbrio, indicando a visão predominante, se houver.
3.  **Estilo de Resposta:** Seja objetiva e bem estruturada. Conclua com uma mensagem apropriada de fé, esperança ou encorajamento baseado nos princípios bíblicos.
4.  **Não Aconselhamento Pessoal Direto:** NÃO forneça aconselhamento para problemas pessoais (financeiros, relacionais, saúde mental, etc.). Ofereça princípios bíblicos gerais e incentive fortemente a busca por orientação pastoral local ou profissional qualificado quando apropriado.
5.  **Reconhecimento de Limites:** Se uma pergunta for excessivamente complexa, fora do escopo teológico definido, ou se a resposta não for claramente estabelecida nas Escrituras ou doutrina da AD, admita a limitação com humildade. EVITE ESPECULAÇÕES. Sugira gentilmente que o usuário consulte um pastor ou líder espiritual experiente.
6.  **Evitar Debate Improdutivo:** Não entre em debates teológicos prolongados ou controversos que não sejam produtivos para o crescimento espiritual. Mantenha o foco na edificação.

Exemplos de Interação (Few-Shot Learning):

Exemplo 1:
Usuário: O que é o batismo no Espírito Santo segundo a Assembleia de Deus?
SophIA: Olá! Segundo a doutrina pentecostal da Assembleia de Deus, o batismo no Espírito Santo é uma bênção maravilhosa e um revestimento de poder do alto, que ocorre após a salvação. Ele é evidenciado inicialmente pelo falar em novas línguas, conforme vemos em Atos 2:4 (ARC): "E todos foram cheios do Espírito Santo e começaram a falar em outras línguas, conforme o Espírito Santo lhes concedia que falassem." Este batismo capacita o crente para um serviço cristão mais eficaz e um testemunho poderoso. É uma promessa para todos os que creem, como Pedro declarou em Atos 2:38-39. Que a busca por essa experiência divina encha seu coração de fé e expectativa!

Exemplo 2:
Usuário: Estou me sentindo muito ansioso ultimamente. O que a Bíblia diz?
SophIA: Compreendo que momentos de ansiedade podem ser difíceis. A Palavra de Deus nos oferece grande conforto e direção. Em Filipenses 4:6-7 (ARC), o apóstolo Paulo nos orienta: "Não estejais inquietos por coisa alguma; antes, as vossas petições sejam em tudo conhecidas diante de Deus, pela oração e súplicas, com ação de graças. E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos sentimentos em Cristo Jesus." Lembre-se de entregar suas preocupações a Deus em oração. Se essa ansiedade persistir ou se tornar muito intensa, é muito importante buscar apoio em seu pastor e, se necessário, em um profissional de saúde. Deus deseja lhe dar paz. Confie Nele!

Exemplo 3 (Pergunta fora do escopo):
Usuário: Qual a melhor forma de investir meu dinheiro?
SophIA: Entendo sua preocupação com a boa administração dos recursos. A Bíblia nos ensina princípios de sabedoria financeira, como a honestidade (Provérbios 16:8 ARC) e a diligência (Provérbios 21:5 ARC). No entanto, como assistente teológica, não posso oferecer aconselhamento financeiro específico. Para decisões de investimento, recomendo que você busque orientação de um profissional da área financeira qualificado. E claro, sempre ore a Deus pedindo sabedoria em todas as suas decisões!
"""
system_instruction = load_system_instruction()

# --- Bloco 6: Definições de Segurança (CVV) ---
keywords_risco = [ "me matar", "me mate", "suicidio", "suicídio", "não aguento mais viver", "quero morrer", "queria morrer", "quero sumir", "desistir de tudo", "acabar com tudo", "fazer mal a mim", "me cortar", "me machucar", "automutilação" ]
resposta_risco_padrao = ( "Sinto muito que você esteja passando por um momento tão difícil e pensando nisso. É muito importante buscar ajuda profissional agora. Por favor, entre em contato com o CVV (Centro de Valorização da Vida) ligando para o número 188. A ligação é gratuita e eles estão disponíveis 24 horas por dia para conversar com você de forma sigilosa. Você não está sozinho(a) e há pessoas prontas para te ouvir." )

# --- Bloco 7: Função para Inicializar o Modelo ---
@st.cache_resource
def init_model():
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=system_instruction
        )
        return model
    except Exception as e:
        st.error(f"Erro grave ao carregar o modelo de IA ('gemini-1.5-flash-latest'): {e}. Verifique a configuração da API Key, o nome do modelo e as instruções do sistema.")
        st.stop()
model = init_model()

# --- Bloco 8: Gerenciamento do Histórico e Sugestões Iniciais ---
# ***** MODIFICADO: Não adiciona mais a mensagem ao histórico aqui *****
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Olá! Sou SophIA. Em que posso ajudá-lo hoje com base na Palavra de Deus e nos ensinamentos da Assembleia de Deus?"}]

if "chat_session" not st.session_state: # Correção: faltava 'in'
    st.session_state.chat_session = model.start_chat(history=[])

if "prompt_from_suggestion" not in st.session_state:
    st.session_state.prompt_from_suggestion = None

if len(st.session_state.messages) <= 1:
    st.markdown("##### Sugestões de temas para explorar:")
    cols = st.columns(3)
    sugestoes = {
        "O que é a Salvação?": "O que é a Salvação pela graça mediante a fé?",
        "A Bíblia é inspirada?": "Como a Assembleia de Deus vê a inspiração da Bíblia?",
        "Quem é Jesus Cristo?": "Fale sobre a divindade e humanidade de Jesus Cristo."
    }
    button_keys = ["sugestao1", "sugestao2", "sugestao3"]

    for i, (texto_botao, pergunta_real) in enumerate(sugestoes.items()):
        if cols[i].button(texto_botao, key=button_keys[i]):
            # APENAS define o prompt que será processado no Bloco 10
            st.session_state.prompt_from_suggestion = pergunta_real
            # Não adiciona mais a st.session_state.messages aqui
            st.rerun()

# --- Bloco 9: Exibição do Histórico ---
# (Sem alterações neste bloco, ele apenas reflete st.session_state.messages)
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and idx > 0 and message["content"] != resposta_risco_padrao:
            feedback_key_base = f"feedback_{idx}"
            col1, col2, col_spacer = st.columns([1,1,8])
            if col1.button("👍", key=f"{feedback_key_base}_up", help="Gostei da resposta!"):
                st.toast("Obrigado pelo seu feedback!", icon="😊")
            if col2.button("👎", key=f"{feedback_key_base}_down", help="Não gostei da resposta."):
                st.toast("Lamento por isso. Seu feedback nos ajuda a melhorar.", icon="😕")

# --- Bloco 10: Input e Lógica Principal ---
# ***** MODIFICADO: Centraliza a adição ao histórico e exibição do prompt do usuário *****

current_prompt = None
# Prioriza input do chat_input
if prompt_input_val := st.chat_input("Digite sua dúvida ou reflexão..."):
    current_prompt = prompt_input_val
# Se não houve chat_input, verifica se há um prompt de sugestão
elif st.session_state.get("prompt_from_suggestion"):
    current_prompt = st.session_state.prompt_from_suggestion
    st.session_state.prompt_from_suggestion = None # Importante: Reseta para não reprocessar

if current_prompt:
    # Adiciona a mensagem do usuário ao histórico global de mensagens (APENAS AQUI)
    st.session_state.messages.append({"role": "user", "content": current_prompt})

    # Exibe a mensagem do usuário na interface (APENAS AQUI)
    with st.chat_message("user"):
        st.markdown(current_prompt)

    # Continua com a lógica de verificação de risco e envio para IA...
    prompt_lower = current_prompt.lower()
    contem_risco = any(keyword in prompt_lower for keyword in keywords_risco)

    if contem_risco:
        # Adiciona a resposta de risco ao histórico antes de exibir
        resposta_assistente_risco = resposta_risco_padrao
        st.session_state.messages.append({"role": "assistant", "content": resposta_assistente_risco})
        with st.chat_message("assistant"):
            st.warning("Importante: Se você está passando por pensamentos difíceis ou de risco, por favor, busque ajuda profissional imediatamente.")
            st.markdown(resposta_assistente_risco)
    else:
        try:
            with st.spinner("SophIA está processando... 📖"):
                response = st.session_state.chat_session.send_message(current_prompt)

            if response.prompt_feedback and response.prompt_feedback.block_reason:
                block_reason = response.prompt_feedback.block_reason
                error_msg_user = f"Sua mensagem não pôde ser processada devido a restrições de conteúdo ({block_reason}). Por favor, reformule sua pergunta ou tente um tema diferente."
                st.session_state.messages.append({"role": "assistant", "content": error_msg_user }) # Adiciona ao histórico
                st.error(error_msg_user) # Exibe o erro
            else:
                bot_response = response.text
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in bot_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

        except genai.types.generation_types.BlockedPromptException as bpe:
            error_msg_user = "Sua mensagem foi bloqueada por nossas políticas de segurança. Por favor, reformule sua pergunta ou tente um tema diferente."
            st.session_state.messages.append({"role": "assistant", "content": error_msg_user})
            st.error(error_msg_user)
            print(f"ERRO DEBUG App: Prompt Bloqueado pela API - {bpe}")
        except Exception as e:
            error_msg_user = "Desculpe, ocorreu um problema técnico ao processar sua mensagem. Tente novamente mais tarde. Se o erro persistir, pode ser uma falha temporária na conexão com a IA."
            # Adiciona uma mensagem de erro genérica ao histórico para o usuário ver
            st.session_state.messages.append({"role": "assistant", "content": "Sinto muito, tive um problema técnico interno. Por favor, tente novamente. 😔"})
            st.error(error_msg_user) # Exibe o erro mais detalhado para o usuário
            print(f"ERRO DEBUG App: Falha ao enviar mensagem para Gemini - {e}") # Log técnico

# --- Bloco 11: Rodapé ---
st.divider()
st.caption("SophIA (v2.2) é uma ferramenta de IA para apoio teológico e espiritual. Lembre-se que a IA é um auxílio e não substitui o estudo pessoal da Palavra, a oração e o conselho pastoral.")
