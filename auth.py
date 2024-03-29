import streamlit as st  # Importing the Streamlit library
from gen_ai_API import user_login
# logging in user by setting session


def start_session(useremail):
    st.session_state.useremail = useremail


def user_auth(userEmail, userPass):
    
    user_auth = user_login(email=userEmail, password=userPass)
    
    if user_auth:
        start_session(userEmail)
    else:
        st.error("Invalid email or password -- RETRY ")


def login():
    """
    Function to handle user login.

    This function displays an email input field and a course selection dropdown. 
    When the user clicks the login button, it stores the entered email in the cookie_manager.

    """
    # User input for email
    useremail = st.text_input(
        "EMAIL:", autocomplete='email', placeholder='(Please enter your mail ID)')
    password = st.text_input(
        "PASSWORD:",autocomplete='password', placeholder='(Please enter your password)',type='password')

    # Dropdown for course selection
    course = st.selectbox('Course', options=['BSCIT'], key='login_course')

    # Button to submit login information
    if  st.button('Log in', disabled= not (password and useremail) ):
        user_auth(userEmail=useremail, userPass=password)

