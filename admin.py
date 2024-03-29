import pandas as pd
import streamlit as st
import requests,os
import json
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(layout='wide')


request_url = os.environ.get('REQUEST_URL')+'/get_logs'

payload = {
    "access_token": os.environ.get('API_ACCESS_TOKEN'),
    "secret_key": os.environ.get('API_SECRET_KEY')
}

headersList = {
    "Accept": "*/*",
    "User-Agent": "Web UI for AI_Chat_bot (https://college-chatbot-1.onrender.com/)",
    "Content-Type": "application/json"
}


def display_logs():
    st.header("Chat Logs")

    response = requests.request(
        'POST', request_url, data=json.dumps(payload),  headers=headersList)
    
    response_json = response.json()
    df = pd.DataFrame(response_json)
    st.write(df)

if __name__ == '__main__':
    display_logs()
