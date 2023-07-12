import requests
import json
from nltk.sentiment import SentimentIntensityAnalyzer


class LinkedinAutomate:
    def __init__(self, access_token):       # init--constructor meathod of the class and is automatically called when an obj of class is creaated
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }    # create a dict called headers--with single key value pair--key(authorization) value(formatted string of access token)
        self.sid = SentimentIntensityAnalyzer()   # linkedin_automate will have access to an instance of the sentiment analysis functionally
        """in summary the code defines a class "linkedinAutomate" with an initializer meathod(__init__)
        that takes an access token parameter, taking attributes access token, headers, sid.
        >>this class is designed to automate tasks realted to linked in using the provided access token and sentiment analysis capabilites"""
    def monitor_competitors_activity(self, competitor_ids):   # self--refering to the instance of the class
        for competitor_id in competitor_ids:    # iterates over each copetitors id in the id's  list
            new_connections = self.get_new_connections(competitor_id)  # calls  getNewConnection meathod with competitor id as argument
            print(f"New Connections for competitor {competitor_id}:")  # print a message indicating the competitors id
            print(new_connections)  # print a list of new connections for the competitor
            print("---")  # seperator for readebility

            for connection_id in new_connections:   # iterate over each connection id in the new connections list
                connection_request_message = self.generate_connection_request(connection_id)  # there is a defined in the class to genereate a connection request message for a specific connection
                response = self.send_connection_request(connection_id, connection_request_message)   # to send a connection request to a specific connection
                print(response)   # recived from sending  the connection request
                print("---")
                """
                summery--the moniterCompetitorsActivity meathod in the linkedin Automate class iterates over a list of competitors ID's
                for each competior, it retrives the new connection prints them and then sends connection request to each new connection
                printing them and then sends connection requests to each new connection  
                printing the response for each new requests 
                it uses additional meathods like
                1.get_new_connections
                2.generate_connection_requests
                3.send_connection_request
                """

    def get_new_connections(self, competitor_id):
        url = f"https://api.linkedin.com/v2/relationships?q=memberId&relationship=connectedTo&start=0&count=10&memberId={competitor_id}"
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)
        """
        build a URL using the connection_id and make a GET request to retrive the info about the connection
        the self.headers contain the necessary authorization info 
        response stored in 'response', and the json data is loaded into data variable
        """

        new_connections = []  # store the extracted connection id's
        for connection in data['elements']:  # for loop  that iterates over each connection in the element (key) of data(dict)
            connection_id = connection['targetInfo']['entityUrn'].split(":")[-1]
            # extract connection id from the connection dict.
            # connection id obtained by splitting the value of 'entityurn' key using ':' delimiter
            # and taking the last element of the resulting list ([-1])
            new_connections.append(connection_id)
            # add the connection id to the connection list

        return new_connections  # returns new connection list

    def generate_connection_request(self, connection_id):
        url = f"https://api.linkedin.com/v2/people/{connection_id}"
        # url  specific to the API to fetch info about the specific connection  by replacing the connectin id
        response = requests.get(url, headers=self.headers)
        # sends HTTP GET request to construct URL using requests
        # header attribute is included to request necessary authorization info
        data = json.loads(response.text)
        # phrases the response from api request as JSON data
        # json.loads()--converts the response text into py dict data

        """
        summary--generateConnectionRequest meathod in the linkedin automate class constructs
        a url specific to a connections info, sends a HTTP GET request to linkedin API using 
        constructed url and auth headers
        this method fetch detailed info about specific connection for further processing
        """


        # Extract relevant information from the connection's profile
        first_name = data['firstName']
        last_name = data['lastName']
        job_title = data['headline']
        about = data['summary']
        recent_posts = data['recentPosts']

        """extract relevant info from connection profile data stored in the data dict
        assign values-- firstname, lastname, headline, summary, recentposts"""

        # Analyze the sentiment of the about section using NLP
        about_sentiment = self.analyze_sentiment(about)  # class has a sentiment analysis functionality available through this method

        # Generate a hyper-personalized connection request message based on the analysis
        if about_sentiment >= 0.5:   # generate a personalized connection request based on the sentiment analysis of the about section
            """if the sentiment score is greater than or equal to 0.5 
                it creates a positive message 
                otherwise creates a more generalized message expressing curiosity"""
            connection_request = f"Hi {first_name} {last_name}, I read your impressive profile and positive about section. I believe we share common interests and goals. Let's connect and explore opportunities together!"
        else:
            connection_request = f"Hi {first_name} {last_name}, I came across your profile and found it intriguing. I would love to connect and learn more about your experiences and perspectives. Looking forward to connecting with you!"

        return connection_request   # return the generated connection request as a result of this method

    def analyze_sentiment(self, text):
        sentiment_scores = self.sid.polarity_scores(text)
        compound_score = sentiment_scores['compound']
        return compound_score
    """
    analyze sentiment meathod in linkedinAutomate class takes text parameter representing text about the competitor
    and performs sentiment analysis on it using polarity score method of sid object mentioned above
    it extracts the compound sentiment score from the result and returns it
    """

    def send_connection_request(self, connection_id, message):  # this method is responsible for sending a connection request to a linkedin user
        url = "https://api.linkedin.com/v2/invitation"
        # this is the url for the linkedin API endpoint where connection requests can be sent

        payload = {
            "invitee": {
                "com.linkedin.voyager.growth.invitation.InviteeProfile": {
                    "profileId": connection_id
                }
            },
            "message": message
        }
        """
        the dict payload contains necessary data to send a connection request 
        it has two keys 
        invitee--contains a nested dict with key as invitee's profile information
        within another nested dict with invitee's profile id and connection id
        message--- a message that can be included in the connection request
        """

        response = requests.post(url, headers=self.headers, json=payload)
        # sends HTTP POST request to linked in API endpoint specified by url variable and request post func

        if response.status_code == 201:     # 201 means the connection was sent sucessfully
            return "Connection request sent successfully."
        else:
            return "Error sending connection request."

    def main_func(self):
        competitor_ids = ["competitor1_id", "competitor2_id"]  # Add the IDs of your competitors here
        self.monitor_competitors_activity(competitor_ids)

        """
        this method with no parameters, has a list of competitor's id 
        then it calls the monitor_competitors_activity method 
        """


access_token = "your_access_token"    # the linkedin API's acess token
LinkedinAutomate(access_token).main_func()   # the linkedin Automate class is called with main_func as instance
