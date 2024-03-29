from dotenv import load_dotenv
import requests
import json
from uuid import uuid4
import os

load_dotenv()

chat_request_url = os.environ.get('REQUEST_URL')+'/chat_ai'
login_request_url = os.environ.get('REQUEST_URL')+'/user_auth'

payload = {
    "access_token": os.environ.get('API_ACCESS_TOKEN'),
    "secret_key": os.environ.get('API_SECRET_KEY')
}

headersList = {
    "Accept": "*/*",
    "User-Agent": "Web UI for AI_Chat_bot (https://college-chatbot-1.onrender.com/)",
    "Content-Type": "application/json"
}

def user_login(email,password):

    payload["login_creds"] = {"email":email, "password": password}
    

    response = requests.request(
        'POST', login_request_url, data=json.dumps(payload),  headers=headersList)
    
    response_json = response.json()
    # Define chat prompt template and output parser
    try:
        answer = response_json['is_valid_user']
    except:
        answer = response_json
    finally:
        return answer



# Function to handle user input and generate response
def ask_ai(user_question, user, id=None):

    if id == None:
        id = str(uuid4())

    payload["queries"] = [{"id": id, "prompt": user_question, "user": user}]
    payload["model"] = "bscit_c_query"


    response = requests.request(
        'POST', chat_request_url, data=json.dumps(payload),  headers=headersList)
    
    response_json = response.json()
    # Define chat prompt template and output parser
    try:
        answer = response_json['response data'][0]['response']
    except:
        answer = response_json
    finally:
        return answer


if __name__ == '__main__':
    user_question = input('Please say what you wanna know ? ')
    user = 'Test user'

    response = ask_ai(user_question,user)
