import streamlit as st
from auth import login  # Importing the login function from the auth module
from chat import load_ui  # Importing the chat_ui function from the chat module

def main():
    """
    Main function to handle the user interaction flow.
    If the user is not logged in, it prompts for login, otherwise starts the chat interface.
    """
    if not st.session_state.get('useremail',default=None):  # If useremail is not present in the cookie_manager
        login()  # Prompt user to login
    else:
        load_ui()  # Start the chat interface

if __name__ =='__main__':
    main()  # Execute the main function if this script is run directly