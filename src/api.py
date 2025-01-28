from requests import get
from dotenv import load_dotenv, set_key
from os import getenv
from datetime import datetime
from time import time
from requests import post
from base64 import b64encode


class API:
    def __init__(self):
        self.token = self.load_token()

    def get(self, path: str):
        res =  get(f"https://api.spotify.com/v1/{path}", headers={"Authorization": f"Bearer {self.token}"})
        if res.status_code == 401:
            raise TimeoutError("O Token de Acesso Expirou")
        return res
    
    
    @staticmethod
    def load_token():
        load_dotenv()
        update_time = datetime.fromtimestamp(int(getenv("TOKEN_LAST_UPDATED")))
        delta = datetime.now().__sub__(update_time)
        if delta.seconds > 60*55:
            return API.reload_token()
        return getenv("ACCESS_TOKEN")


    @staticmethod
    def reload_token():
        client_creds = f"{getenv("CLIENT_ID")}:{getenv("CLIENT_SECRET")}"
        client_creds_b64 = b64encode(client_creds.encode()).decode()
        
        # Define the headers and data payload for the request
        headers = {
            "Authorization": f"Basic {client_creds_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials"
        }
        
        # Make the POST request to Spotify's token endpoint
        response = post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        
        # Check the response
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]

            set_key(".env", "TOKEN_LAST_UPDATED", str(int(time())))
            set_key(".env", "ACCESS_TOKEN", access_token)

            print("Retrieved access token access token.")
            return access_token
        else:
            print("Failed to retrieve access token.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
