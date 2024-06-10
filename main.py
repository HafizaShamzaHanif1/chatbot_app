import streamlit as st
import google.generativeai as ggi

fetched_api_key = "AIzaSyDp17AjWrSCKyr35QYfIt6c2lZVHRJwyvY"  
if not fetched_api_key:
    st.error("API Key not found. Please check your .env file.")
    st.stop()

ggi.configure(api_key=fetched_api_key)

model = ggi.GenerativeModel("gemini-pro")
chat = model.start_chat()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def LLM_Response(question):
    career_counseling_context = "Considering career counseling in Pakistan, "
    full_question = career_counseling_context + question
    try:
        response = chat.send_message(full_question, stream=True)
        full_response = ''.join([word.text for word in response])
    except Exception as e:
        full_response = "An error occurred: " + str(e)
    return full_response

st.markdown("""
    <style>
    .main {
        background-image: url("https://cdn.wallpapersafari.com/0/62/TA4eir.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        padding: 20px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput input {
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        font-size: 16px;
    }
    .chat-history {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        max-height: 400px;
        overflow: auto;
        margin-top: 20px;
    }
    .chat-entry {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #e6f7ff;
        color: #005b96;
        text-align: left;
    }
    .bot-message {
        background-color: #005b96;
        color: #ffffff;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Career Counseling Chat Application")

with st.form(key='my_form'):
    user_question = st.text_input("Ask a question about career counseling:", key="user_input")
    submit_button = st.form_submit_button(label='Submit')

if submit_button and user_question:
    answer = LLM_Response(user_question)
    st.session_state.chat_history.append(("You", user_question))
    st.session_state.chat_history.append(("Career Hub", answer))

chat_history_html = '<div class="chat-history">'
for i in range(len(st.session_state.chat_history) - 1, -1, -2):
    if i - 1 >= 0:
        question_speaker, question_message = st.session_state.chat_history[i - 1]
        answer_speaker, answer_message = st.session_state.chat_history[i]
        
        chat_history_html += f"""
        <div class="chat-entry user-message"><b>{question_speaker}:</b> {question_message}</div>
        <div class="chat-entry bot-message"><b>{answer_speaker}:</b> {answer_message}</div>
        """
chat_history_html += "</div>"

st.markdown(chat_history_html, unsafe_allow_html=True)
