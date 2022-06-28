from flask import current_app

from vendors.helper import Helper


class Cognito:
    def __init__(self):
        self.client_id = current_app.config["COGNITO_CLIENT_ID"]
        self.authflow = current_app.config["AUTH_FLOW"]
        self.session = Helper.get_session()
        self.client = self.get_client()

    def get_client(self):
        client = self.session.client('cognito-idp')
        return client

    def authorize(self, username, password):
        return self.client.initiate_auth(
            ClientId=self.client_id,
            AuthFlow=self.authflow,
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            })
