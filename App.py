import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Batmochila IA", page_icon="🦇")
st.title("🦇 Batmochila: O Chat Ranzinza")
st.caption("A IA do Morcego de Gotham de mau humor com você.")

# Configura a chave da API do Gemini (Substitua pela sua chave real depois)
# Para pegar uma de graça, pesquise por "Google AI Studio" no navegador
GOOGLE_API_KEY = "SUA_CHAVE_AQUI"
genai.configure(api_key=GOOGLE_API_KEY)

# Aqui definimos a PERSONAGEM da IA (O cérebro)
instrucao_personalidade = (
    "Você é o Batman, mas é ranzinza, irônico e está de mau humor. "
    "Você responde de forma curta, séria e vive reclamando que o usuário está te "
    "fazendo perder tempo enquanto Gotham está cheia de criminosos. Use gírias de herói "
    "e responda sempre em português de forma cômica."
)

# Inicializa o histórico de mensagens no Streamlit para ele não esquecer a conversa
if "historico" not in st.session_state:
    st.session_state.historico = []

# Exibe o histórico de mensagens na tela (Os balões do chatbot)
for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])

# Barra de digitação do Chatbot
if prompt := st.chat_input("Diga algo para o Morcego..."):
    
    # 1. Mostra o que você digitou na tela
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.historico.append({"role": "user", "content": prompt})

    # 2. Envia para a IA processar a resposta com a personalidade
    with st.spinner("O morcego está pensando (e reclamando)..."):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=instrucao_personalidade
            )
            
            # Formata o histórico para a IA entender o contexto
            conversa = model.start_chat(history=[])
            resposta_ia = conversa.send_message(prompt).text
            
            # 3. Mostra a resposta da IA no chatbot
            with st.chat_message("assistant"):
                st.write(resposta_ia)
            st.session_state.historico.append({"role": "assistant", "content": resposta_ia})
            
        except Exception as e:
            st.error(f"Erro ao falar com a IA: {e}. Verifique se configurou a sua API KEY!")

