import requests
import json
from nltk.sentiment import SentimentIntensityAnalyzer

class LinkedinAutomate:
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        self.sid = SentimentIntensityAnalyzer()

    def monitor_competitors_activity(self, competitor_ids):
        # Monitor the activity of each competitor
        for competitor_id in competitor_ids:
            new_connections = self.get_new_connections(competitor_id)
            print(f"New Connections for competitor {competitor_id}:")
            print(new_connections)
            print("---")

            # Send connection requests to new connections
            for connection_id in new_connections:
                connection_request_message = self.generate_connection_request(connection_id)
                response = self.send_connection_request(connection_id, connection_request_message)
                print(response)
                print("---")

    def get_new_connections(self, competitor_id):
        url = f"https://api.linkedin.com/v2/relationships?q=memberId&relationship=connectedTo&start=0&count=10&memberId={competitor_id}"
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)

        new_connections = []
        # Extract connection IDs from the API response
        for connection in data.get('elements', []):
            connection_id = connection['targetInfo']['entityUrn'].split(":")[-1]
            new_connections.append(connection_id)

        return new_connections

    def generate_connection_request(self, connection_id):
        url = f"https://api.linkedin.com/v2/people/{connection_id}"
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)

        # Extract relevant information from the connection's profile
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        job_title = data.get('headline', '')
        about = data.get('summary', '')
        recent_posts = data.get('recentPosts', [])

        # Analyze the sentiment of the about section using NLP
        about_sentiment = self.analyze_sentiment(about)

        # Generate a hyper-personalized connection request message based on the analysis
        if about_sentiment >= 0.5:
            connection_request = f"Hi {first_name} {last_name}, I read your impressive profile and positive about section. I believe we share common interests and goals. Let's connect and explore opportunities together!"
        else:
            connection_request = f"Hi {first_name} {last_name}, I came across your profile and found it intriguing. I would love to connect and learn more about your experiences and perspectives. Looking forward to connecting with you!"

        return connection_request

    def analyze_sentiment(self, text):
        sentiment_scores = self.sid.polarity_scores(text)
        compound_score = sentiment_scores['compound']
        return compound_score

    def send_connection_request(self, connection_id, message):
        url = "https://api.linkedin.com/v2/invitation"

        payload = {
            "invitee": {
                "com.linkedin.voyager.growth.invitation.InviteeProfile": {
                    "profileId": connection_id
                }
            },
            "message": message
        }

        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 201:
            return "Connection request sent successfully."
        else:
            return "Error sending connection request."

    def main_func(self):
        competitor_ids = ["sridileep", "karthik-chennuri-a5577519b"]
        self.monitor_competitors_activity(competitor_ids)


access_token = "I94UiysljveSlniYY_vKjQ"
LinkedinAutomate(access_token).main_func()

