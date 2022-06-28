from vendors.cognito import Cognito
from vendors.dynamodb import DynamoDB
from entities.resident import Resident


class UserAuth:

    def __init__(self):
        self.cognito = Cognito()
        self.dynamo = DynamoDB()
        self.table_name = "user"

    def check_if_admin(self, username, password):
        try:
            self.cognito.authorize(username, password)
        except self.cognito.client.exceptions.NotAuthorizedException:
            return None
        except self.cognito.client.exceptions.UserNotConfirmedException:
            return None
        except Exception as e:
            return None
        return "Admin"

    def scan_db_for_user(self, username, password):
        resident_obj = Resident()
        residents = resident_obj.get_all_residents()
        authorized_user = [resident for resident in residents
                           if resident["user_email"] == username and resident["user_password"] == password]
        return authorized_user
