from secrets import refresh_token, base_64
import requests
import json

class Refresh:

    def __init__(self) -> None:
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):

        print("In hereee")
        query = "https://accounts.spotifycom/api/token"

        response = requests.post(query,
                                data={"grant_type": "refresh_token",
                                      "refresh_token": self.refresh_token},
                                headers={"Authorization": "Basic " + self.base_64})
        print("Did I make it here?")
        response_json = response.json()
        
        return response_json["accress_token"]

a = Refresh()
a.refresh()    
    