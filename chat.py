import os
from datetime import datetime

from admin import display_logs
from gen_ai_API import ask_ai
import pandas as pd
import streamlit as st

# GLOBAL Variables
admins = ['rohitadak02@gmail.com']
useChat = True


# Controls for ADMINS
def admin_controls():
    global useChat
    useChat = not useChat

# Function for logging chat interactions
def logger(user, prompt, response):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists('chat_logs.csv'):
        # Create an empty DataFrame with the specified columns
        df = pd.DataFrame(columns=['Timestamp', 'User', 'Prompt', 'Response'])

        # Write the DataFrame to a CSV file
        df.to_csv('chat_logs.csv', index=False)

    data = {'Timestamp': current_time, 'User': [
        user], 'Prompt': [prompt], 'Response': response}

    pd.DataFrame(data, columns=['Timestamp', 'User', 'Prompt', 'Response']).to_csv(
        'chat_logs.csv', mode='a', index=False, header=False)


# logout user by deleting user session
def delete_session():
    del st.session_state['useremail']


# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hey Hi!!"}]


# Load UI for chatting
def chat_ui():
    # Main chat interface
    st.title("Ask me your college doubts")
    st.write("Welcome to the chat!")

    # Initialize chat history if not exists
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": """Hey Hello!! \n 
 **You can ask me Questions like:** 
 - Syllabus for 2nd semester
 - Time table for regular examination schedules for Sem-6
 - Time table and ATKT examination schedules for Sem-6
 - Need notes for ITSM"""}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # Bot response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_ai(prompt,user=st.session_state['useremail'])
                placeholder = st.empty()
                placeholder.markdown(response)
        if response is not None:
            message = {"role": "assistant", "content": response}
            logger(st.session_state['useremail'], prompt, response)
            st.session_state.messages.append(message)


# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hey Hi!!"}]


# UI for chat interaction
def load_ui():
    global useChat
    # Sidebar menu
    with st.sidebar:
        st.title("Menu:")
        user_tab, admin_tab = st.tabs(['user', 'admins'])
        with user_tab:
            # Check if user is logged in
            if st.session_state['useremail']:
                # CSS to position elements at the bottom
                st.markdown(
                    """
                    <style>
                    .sidebar .element-container:last-child {
                        position: absolute;
                        bottom: 0;
                        width: 100%;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

            st.selectbox('Course', options=['BSCIT'])
            st.selectbox('Mode', options=['QnA'])
            clear_chat_container = st.container()
            with clear_chat_container:
                st.button('Clear Chat History', on_click=clear_chat_history)
                st.button('Log out', on_click=delete_session)
        with admin_tab:
            if not st.session_state.useremail in admins:
                useChat = True
            btn_name = "Check Logs" if useChat else "Use ChatBot"
            st.button(btn_name, on_click=admin_controls,
                      disabled=not st.session_state.useremail in admins, help='Hope you are an ADMIN')

    if useChat:
        chat_ui()
    else:
        display_logs()


if __name__ == '__main__':
    # Run the chat UI
    load_ui()
